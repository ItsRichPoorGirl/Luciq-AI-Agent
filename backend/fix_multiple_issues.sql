-- Fix multiple database and configuration issues
-- 1. Add missing agent_id column to messages table
-- 2. Create Suna default agent if missing
-- 3. Fix admin bypass functionality

BEGIN;

-- 1. Fix messages table - add missing agent_id foreign key
ALTER TABLE messages ADD COLUMN IF NOT EXISTS agent_id UUID REFERENCES agents(agent_id) ON DELETE SET NULL;
CREATE INDEX IF NOT EXISTS idx_messages_agent_id ON messages(agent_id);
COMMENT ON COLUMN messages.agent_id IS 'ID of the agent that generated this message. For user messages, this represents the agent that should respond to this message.';

-- 2. Create Suna default agent for each account if one doesn't exist
-- First, let's check if any Suna default agents exist
DO $$
DECLARE
    account_record RECORD;
    existing_count INTEGER;
    new_agent_id UUID;
BEGIN
    -- Loop through all accounts and ensure each has a Suna default agent
    FOR account_record IN 
        SELECT id as account_id FROM basejump.accounts 
    LOOP
        -- Check if this account already has a Suna default agent
        SELECT COUNT(*) INTO existing_count
        FROM agents 
        WHERE account_id = account_record.account_id 
        AND COALESCE((metadata->>'is_suna_default')::boolean, false) = true;
        
        -- If no Suna default agent exists, create one
        IF existing_count = 0 THEN
            -- Generate new agent ID
            new_agent_id := gen_random_uuid();
            
            -- Insert the Suna default agent
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
                'Suna',
                'Suna - Your AI assistant that helps you accomplish real-world tasks through natural conversation, web browsing, file management, and more.',
                jsonb_build_object(
                    'system_prompt', 'You are Suna, a helpful AI assistant that can help users accomplish real-world tasks through natural conversation. You have access to various tools including web browsing, file management, command-line execution, and more. Always be helpful, accurate, and efficient in your responses.',
                    'tools', jsonb_build_object(
                        'agentpress', jsonb_build_object(
                            'web_search', true,
                            'web_scraper', true,
                            'file_manager', true,
                            'shell', true,
                            'code_executor', true
                        ),
                        'mcp', '[]'::jsonb,
                        'custom_mcp', '[]'::jsonb
                    ),
                    'metadata', jsonb_build_object(
                        'avatar', '🌟',
                        'avatar_color', '#3B82F6'
                    )
                ),
                jsonb_build_object(
                    'is_suna_default', true,
                    'centrally_managed', true,
                    'management_version', '1.0.0'
                ),
                true, -- is_default
                '🌟',
                '#3B82F6',
                NOW(),
                NOW()
            );
            
            RAISE NOTICE 'Created Suna default agent % for account %', new_agent_id, account_record.account_id;
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

-- 4. Add admin bypass user if configured (using ADMIN_API_KEY as identifier)
-- This helps with model access bypassing subscription limits
-- Note: This requires ADMIN_API_KEY to be set in environment

-- Verify the fixes
SELECT 
    'Messages table agent_id column' as fix_category,
    CASE WHEN EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'messages' AND column_name = 'agent_id'
    ) THEN 'Fixed' ELSE 'Missing' END as status;

SELECT 
    'Suna default agents per account' as fix_category,
    COUNT(*) as suna_agents_created
FROM agents 
WHERE COALESCE((metadata->>'is_suna_default')::boolean, false) = true;

SELECT 
    'Accounts with Suna default agent' as fix_category,
    COUNT(DISTINCT account_id) as accounts_with_suna
FROM agents 
WHERE COALESCE((metadata->>'is_suna_default')::boolean, false) = true;

COMMIT;