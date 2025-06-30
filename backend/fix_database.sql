-- Fix database schema issues
-- This script applies the missing migrations for agents and workflows tables

-- Apply upstream migrations in correct order
-- This script applies the missing migrations from upstream

-- 1. Apply agents table migration (from upstream)
BEGIN;

-- Create agents table for storing agent configurations
CREATE TABLE IF NOT EXISTS agents (
    agent_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    account_id UUID NOT NULL REFERENCES basejump.accounts(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    system_prompt TEXT NOT NULL,
    configured_mcps JSONB DEFAULT '[]'::jsonb,
    agentpress_tools JSONB DEFAULT '{}'::jsonb,
    is_default BOOLEAN DEFAULT false,
    avatar VARCHAR(10),
    avatar_color VARCHAR(7),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Add indexes for performance on agents table
CREATE INDEX IF NOT EXISTS idx_agents_account_id ON agents(account_id);
CREATE INDEX IF NOT EXISTS idx_agents_is_default ON agents(is_default);
CREATE INDEX IF NOT EXISTS idx_agents_created_at ON agents(created_at);

-- Add unique constraint to ensure only one default agent per account
CREATE UNIQUE INDEX IF NOT EXISTS idx_agents_account_default ON agents(account_id, is_default) WHERE is_default = true;

-- Create agent_versions table if it doesn't exist
CREATE TABLE IF NOT EXISTS agent_versions (
    version_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    agent_id UUID NOT NULL REFERENCES agents(agent_id) ON DELETE CASCADE,
    version_number INTEGER NOT NULL,
    version_name VARCHAR(50) NOT NULL,
    system_prompt TEXT NOT NULL,
    configured_mcps JSONB DEFAULT '[]'::jsonb,
    custom_mcps JSONB DEFAULT '[]'::jsonb,
    agentpress_tools JSONB DEFAULT '{}'::jsonb,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    created_by UUID REFERENCES basejump.accounts(id),
    
    UNIQUE(agent_id, version_number),
    UNIQUE(agent_id, version_name)
);

-- Add current version tracking to agents table
ALTER TABLE agents ADD COLUMN IF NOT EXISTS current_version_id UUID REFERENCES agent_versions(version_id);
ALTER TABLE agents ADD COLUMN IF NOT EXISTS version_count INTEGER DEFAULT 1;

-- Add index for current version
CREATE INDEX IF NOT EXISTS idx_agents_current_version ON agents(current_version_id);

-- Add agent_id column to threads table if it doesn't exist
DO $$ 
BEGIN
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                   WHERE table_name='threads' AND column_name='agent_id') THEN
        ALTER TABLE threads ADD COLUMN agent_id UUID REFERENCES agents(agent_id) ON DELETE SET NULL;
        CREATE INDEX idx_threads_agent_id ON threads(agent_id);
    END IF;
END $$;

-- Add version tracking to threads
ALTER TABLE threads ADD COLUMN IF NOT EXISTS agent_version_id UUID REFERENCES agent_versions(version_id);

-- Create workflows table if it doesn't exist
CREATE TABLE IF NOT EXISTS workflows (
    workflow_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    account_id UUID NOT NULL REFERENCES basejump.accounts(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    flow_data JSONB NOT NULL DEFAULT '{}'::jsonb,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Add indexes for workflows
CREATE INDEX IF NOT EXISTS idx_workflows_account_id ON workflows(account_id);
CREATE INDEX IF NOT EXISTS idx_workflows_is_active ON workflows(is_active);
CREATE INDEX IF NOT EXISTS idx_workflows_created_at ON workflows(created_at);

-- Enable RLS on tables
ALTER TABLE agents ENABLE ROW LEVEL SECURITY;
ALTER TABLE agent_versions ENABLE ROW LEVEL SECURITY;
ALTER TABLE workflows ENABLE ROW LEVEL SECURITY;

-- Basic RLS policies for agents
DROP POLICY IF EXISTS agents_select_own ON agents;
CREATE POLICY agents_select_own ON agents
    FOR SELECT
    USING (basejump.has_role_on_account(account_id));

DROP POLICY IF EXISTS agents_insert_own ON agents;
CREATE POLICY agents_insert_own ON agents
    FOR INSERT
    WITH CHECK (basejump.has_role_on_account(account_id, 'owner'));

DROP POLICY IF EXISTS agents_update_own ON agents;
CREATE POLICY agents_update_own ON agents
    FOR UPDATE
    USING (basejump.has_role_on_account(account_id, 'owner'));

DROP POLICY IF EXISTS agents_delete_own ON agents;
CREATE POLICY agents_delete_own ON agents
    FOR DELETE
    USING (basejump.has_role_on_account(account_id, 'owner') AND is_default = false);

-- Basic RLS policies for workflows
DROP POLICY IF EXISTS workflows_select_own ON workflows;
CREATE POLICY workflows_select_own ON workflows
    FOR SELECT
    USING (basejump.has_role_on_account(account_id));

DROP POLICY IF EXISTS workflows_insert_own ON workflows;
CREATE POLICY workflows_insert_own ON workflows
    FOR INSERT
    WITH CHECK (basejump.has_role_on_account(account_id, 'owner'));

DROP POLICY IF EXISTS workflows_update_own ON workflows;
CREATE POLICY workflows_update_own ON workflows
    FOR UPDATE
    USING (basejump.has_role_on_account(account_id, 'owner'));

DROP POLICY IF EXISTS workflows_delete_own ON workflows;
CREATE POLICY workflows_delete_own ON workflows
    FOR DELETE
    USING (basejump.has_role_on_account(account_id, 'owner'));

COMMIT; 