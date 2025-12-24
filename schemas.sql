-- Core: Multi-tenant separation 
CREATE TABLE tenants (
    id UUID PRIMARY KEY,
    name TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP 
);

-- Core CRM entities 
CREATE TABLE contacts (
    id UUID PRIMARY KEY,
    tenant_id UUID REFERENCES tenants(id) NOT NULL, -- Non-negotiable isolation 
    first_name TEXT,
    last_name TEXT,
    email TEXT,
    phone TEXT,
    is_patient BOOLEAN DEFAULT FALSE -- Shared core adaptability 
);

CREATE TABLE deals (
    id UUID PRIMARY KEY,
    tenant_id UUID REFERENCES tenants(id) NOT NULL,
    title TEXT NOT NULL,
    amount DECIMAL(12, 2),
    stage TEXT DEFAULT 'Discovery',
    contact_id UUID REFERENCES contacts(id)
);

-- Vertical Module: Clinics 
CREATE TABLE appointments (
    id UUID PRIMARY KEY,
    tenant_id UUID REFERENCES tenants(id) NOT NULL, -- Tenant-scoped
    patient_id UUID REFERENCES contacts(id),
    scheduled_at TIMESTAMP NOT NULL,
    treatment_type TEXT,
    practitioner_id UUID, -- For RBAC/Staff tracking 
    notes TEXT,
    status TEXT DEFAULT 'Scheduled'
);

-- Audit logs for security basics 
CREATE TABLE audit_logs (
    id SERIAL PRIMARY KEY,
    tenant_id UUID REFERENCES tenants(id),
    user_id UUID,
    action TEXT,
    entity_type TEXT,
    entity_id UUID,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);