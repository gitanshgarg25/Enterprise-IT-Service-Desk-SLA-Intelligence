-- ============================================================================
-- Script 01: Database Schema Creation and Data Import
-- Project: Enterprise IT Service Desk & SLA Intelligence Platform
-- Target Database: SQLite 3
-- Author: Data Analytics Mentor
-- Description: Defines fact and dimension tables, constraints, indexes,
--              and provides native SQLite import instructions.
-- ============================================================================

-- Enable Foreign Key constraints
PRAGMA foreign_keys = ON;

-- ----------------------------------------------------------------------------
-- 1. Drop existing tables if re-running
-- ----------------------------------------------------------------------------
DROP TABLE IF EXISTS fact_tickets;
DROP TABLE IF EXISTS dim_priority_sla;
DROP TABLE IF EXISTS dim_support_team;

-- ----------------------------------------------------------------------------
-- 2. Create Dimension: Priority & SLA Definitions
-- ----------------------------------------------------------------------------
CREATE TABLE dim_priority_sla (
    Priority                    VARCHAR(10) PRIMARY KEY,
    SLA_Target_Hours            DECIMAL(4,1) NOT NULL,
    Severity_Level              VARCHAR(5) NOT NULL,
    Business_Impact_Description TEXT NOT NULL
);

-- ----------------------------------------------------------------------------
-- 3. Create Dimension: Support Teams
-- ----------------------------------------------------------------------------
CREATE TABLE dim_support_team (
    Support_Team                VARCHAR(40) PRIMARY KEY,
    Support_Tier                VARCHAR(10) NOT NULL,
    Core_Specialization         TEXT NOT NULL
);

-- ----------------------------------------------------------------------------
-- 4. Create Fact Table: ITSM Tickets
-- ----------------------------------------------------------------------------
CREATE TABLE fact_tickets (
    Ticket_ID                   VARCHAR(16) PRIMARY KEY,
    Created_Date                DATETIME NOT NULL,
    Resolved_Date               DATETIME,
    Status                      VARCHAR(20) NOT NULL,
    Priority                    VARCHAR(10) NOT NULL,
    Category                    VARCHAR(35) NOT NULL,
    Subcategory                 VARCHAR(35) NOT NULL,
    Support_Team                VARCHAR(40) NOT NULL,
    Assigned_Agent              VARCHAR(30) NOT NULL,
    Department                  VARCHAR(30) NOT NULL,
    SLA_Target_Hours            DECIMAL(4,1) NOT NULL,
    Actual_Resolution_Hours     DECIMAL(6,2),
    SLA_Status                  VARCHAR(25) NOT NULL,
    Customer_Satisfaction_Score INTEGER,
    Reopened_Flag               INTEGER NOT NULL DEFAULT 0,
    Escalated_Flag              INTEGER NOT NULL DEFAULT 0,
    FOREIGN KEY (Priority)     REFERENCES dim_priority_sla (Priority),
    FOREIGN KEY (Support_Team) REFERENCES dim_support_team (Support_Team)
);

-- ----------------------------------------------------------------------------
-- 5. Performance Indexes
-- ----------------------------------------------------------------------------
CREATE INDEX idx_tickets_created_date ON fact_tickets (Created_Date);
CREATE INDEX idx_tickets_status ON fact_tickets (Status);
CREATE INDEX idx_tickets_priority ON fact_tickets (Priority);
CREATE INDEX idx_tickets_category ON fact_tickets (Category);
CREATE INDEX idx_tickets_support_team ON fact_tickets (Support_Team);
CREATE INDEX idx_tickets_sla_status ON fact_tickets (SLA_Status);

-- ----------------------------------------------------------------------------
-- 6. SQLite CLI Data Import Instructions
-- To import via sqlite3 command line:
--
-- sqlite3 data/itsm_service_desk.db
-- .mode csv
-- .headers on
-- .import --skip 1 data/cleaned/dim_priority_sla.csv dim_priority_sla
-- .import --skip 1 data/cleaned/dim_support_team.csv dim_support_team
-- .import --skip 1 data/cleaned/itsm_tickets_cleaned.csv fact_tickets
-- ----------------------------------------------------------------------------
