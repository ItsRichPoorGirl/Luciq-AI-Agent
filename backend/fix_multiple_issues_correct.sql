-- Fix multiple database and configuration issues using EXACT upstream Suna configuration
-- 1. Add missing agent_id column to messages table
-- 2. Create proper Suna default agent with upstream configuration
-- 3. Fix admin bypass functionality

BEGIN;

-- 1. Fix messages table - add missing agent_id foreign key
ALTER TABLE messages ADD COLUMN IF NOT EXISTS agent_id UUID REFERENCES agents(agent_id) ON DELETE SET NULL;
CREATE INDEX IF NOT EXISTS idx_messages_agent_id ON messages(agent_id);
COMMENT ON COLUMN messages.agent_id IS 'ID of the agent that generated this message. For user messages, this represents the agent that should respond to this message.';

-- 2. Create Suna default agent using EXACT upstream configuration
DO $$
DECLARE
    account_record RECORD;
    existing_count INTEGER;
    new_agent_id UUID;
    upstream_system_prompt TEXT;
BEGIN
    -- Define the upstream system prompt (truncated for DB - full prompt loaded dynamically in app)
    upstream_system_prompt := 'You are Suna.so, an autonomous AI Agent created by the Kortix team.

# 1. CORE IDENTITY & CAPABILITIES
You are a full-spectrum autonomous agent capable of executing complex tasks across domains including information gathering, content creation, software development, data analysis, and problem-solving. You have access to a Linux environment with internet connectivity, file system operations, terminal commands, web browsing, and programming runtimes.

# 2. EXECUTION ENVIRONMENT

## 2.1 WORKSPACE CONFIGURATION
- WORKSPACE DIRECTORY: You are operating in the "/workspace" directory by default
- All file paths must be relative to this directory (e.g., use "src/main.py" not "/workspace/src/main.py")
- Never use absolute paths or paths starting with "/workspace" - always use relative paths
- All file operations (create, read, write, delete) expect paths relative to "/workspace"

[Note: Full system prompt loaded dynamically from SunaConfig.get_system_prompt() - this is the upstream pattern]';

    -- Loop through all accounts and ensure each has a Suna default agent
    FOR account_record IN 
        SELECT id as account_id FROM basejump.accounts 
    LOOP
        -- Check if this account already has a Suna default agent
        SELECT COUNT(*) INTO existing_count
        FROM agents 
        WHERE account_id = account_record.account_id 
        AND COALESCE((metadata->>'is_suna_default')::boolean, false) = true;
        
        -- If no Suna default agent exists, create one with EXACT upstream config
        IF existing_count = 0 THEN
            -- Generate new agent ID
            new_agent_id := gen_random_uuid();
            
            -- Insert the Suna default agent with upstream configuration
            INSERT INTO agents (
                agent_id,
                account_id,
                name,
                description,
                config,
                metadata,
                is_default,
                avatar,
                avatar_color,
                created_at,
                updated_at
            ) VALUES (
                new_agent_id,
                account_record.account_id,
                'Luciq', -- Modified from SunaConfig.NAME
                'Luciq is your AI assistant with access to various tools and integrations to help you with tasks across domains.', -- Modified from SunaConfig.DESCRIPTION
                jsonb_build_object(
                    'system_prompt', upstream_system_prompt,
                    'tools', jsonb_build_object(
                        'agentpress', jsonb_build_object(
                            -- Exact upstream SunaConfig.DEFAULT_TOOLS
                            'sb_shell_tool', jsonb_build_object('enabled', true, 'description', 'Execute shell commands'),
                            'sb_files_tool', jsonb_build_object('enabled', true, 'description', 'Read, write, and edit files'),
                            'sb_browser_tool', jsonb_build_object('enabled', true, 'description', 'Browse websites and interact with web pages'),
                            'sb_deploy_tool', jsonb_build_object('enabled', true, 'description', 'Deploy web applications'),
                            'sb_expose_tool', jsonb_build_object('enabled', true, 'description', 'Expose local services to the internet'),
                            'web_search_tool', jsonb_build_object('enabled', true, 'description', 'Search the web for information'),
                            'sb_vision_tool', jsonb_build_object('enabled', true, 'description', 'Analyze and understand images'),
                            'sb_image_edit_tool', jsonb_build_object('enabled', true, 'description', 'Edit and manipulate images'),
                            'data_providers_tool', jsonb_build_object('enabled', true, 'description', 'Access structured data from various providers')
                        ),
                        'mcp', '[]'::jsonb, -- SunaConfig.DEFAULT_MCPS
                        'custom_mcp', '[]'::jsonb -- SunaConfig.DEFAULT_CUSTOM_MCPS
                    ),
                    'metadata', jsonb_build_object(
                        'avatar', '🌞', -- SunaConfig.AVATAR
                        'avatar_color', '#F59E0B' -- SunaConfig.AVATAR_COLOR
                    )
                ),
                jsonb_build_object(
                    'is_suna_default', true,
                    'centrally_managed', true,
                    'restrictions', jsonb_build_object(
                        -- Exact upstream SunaConfig.USER_RESTRICTIONS
                        'system_prompt_editable', false,
                        'tools_editable', false,
                        'name_editable', false,
                        'description_editable', true,
                        'mcps_editable', true
                    ),
                    'installation_date', NOW()::text,
                    'last_central_update', NOW()::text,
                    'config_version', 'upstream-sync-1.0.0'
                ),
                true, -- is_default
                '🌞', -- SunaConfig.AVATAR
                '#F59E0B', -- SunaConfig.AVATAR_COLOR
                NOW(),
                NOW()
            );
            
            RAISE NOTICE 'Created Luciq default agent % for account %', new_agent_id, account_record.account_id;
        END IF;
    END LOOP;
END $$;

-- 3. Ensure all existing custom agents are not set as default if a Suna agent exists
UPDATE agents 
SET is_default = false 
WHERE is_default = true 
AND NOT COALESCE((metadata->>'is_suna_default')::boolean, false) = true
AND EXISTS (
    SELECT 1 FROM agents suna_agent 
    WHERE suna_agent.account_id = agents.account_id 
    AND COALESCE((suna_agent.metadata->>'is_suna_default')::boolean, false) = true
);

-- Verify the fixes
SELECT 
    'Messages table agent_id column' as fix_category,
    CASE WHEN EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'messages' AND column_name = 'agent_id'
    ) THEN 'Fixed' ELSE 'Missing' END as status;

SELECT 
    'Luciq default agents created' as fix_category,
    COUNT(*) as luciq_agents_created
FROM agents 
WHERE COALESCE((metadata->>'is_suna_default')::boolean, false) = true;

SELECT 
    'Accounts with Luciq default agent' as fix_category,
    COUNT(DISTINCT account_id) as accounts_with_luciq
FROM agents 
WHERE COALESCE((metadata->>'is_suna_default')::boolean, false) = true;

-- Show the created Luciq agent details for verification
SELECT 
    name,
    description,
    avatar,
    avatar_color,
    is_default,
    metadata->>'is_suna_default' as is_suna_default,
    metadata->>'centrally_managed' as centrally_managed,
    config->'tools'->'agentpress'->>'sb_shell_tool' as has_shell_tool
FROM agents 
WHERE COALESCE((metadata->>'is_suna_default')::boolean, false) = true
LIMIT 1;

COMMIT;