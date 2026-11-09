-- ============================================================================
-- JFA-Predictive Credit Risk Engine: Enterprise SQL Portfolio Audits
-- Database: MySQL 8.4 (`credit.borrowers` — 149,999 records)
-- Operator: Raj Dwarkanath Jadhav (Student ID #979948191, University of Auckland Feb 2027)
-- ============================================================================

-- ----------------------------------------------------------------------------
-- 1. Dynamic Feature Persistence: Stored Generated Column
-- Eliminates runtime delinquency calculation latency across 150,000 borrowers.
-- Execution: 0.73s
-- ----------------------------------------------------------------------------
ALTER TABLE borrowers 
ADD COLUMN total_late_events INT 
GENERATED ALWAYS AS (past_due_30_59 + late_90_days + past_due_60_89) STORED;


-- ----------------------------------------------------------------------------
-- 2. The "Thin File" Paradox (Undisclosed Income Audit)
-- Investigates 29,731 unrecorded income loans. 
-- Finding: Borrowers with <= 2 lines default at 10-12% (double baseline),
-- proving <= 2 lines indicates a "Thin File" credit-rebuilder profile.
-- ----------------------------------------------------------------------------
SELECT 
    CASE 
        WHEN open_credit_lines <= 2 THEN 'Thin File (<= 2 Lines)'
        ELSE 'Seasoned Bureau (>= 3 Lines)'
    END AS credit_profile,
    COUNT(*) AS borrower_count,
    ROUND(AVG(serious_dlq_2yrs) * 100, 2) AS default_rate_pct
FROM borrowers
WHERE monthly_income_missing = 1
GROUP BY credit_profile;


-- ----------------------------------------------------------------------------
-- 3. The 8-Row Unified Executive Risk Grid (Income vs Leverage)
-- Tests whether high monthly income cushions borrowers against high debt.
-- Finding: High debt (>50%) causes a +140% default surge (4.30% to 10.36%)
-- even for earners making >= $6,000/month.
-- ----------------------------------------------------------------------------
SELECT 
    CASE 
        WHEN monthly_income_missing = 1 THEN '4. Undisclosed Income'
        WHEN monthly_income >= 6000 THEN '1. High Income (>= $6k)'
        WHEN monthly_income >= 3000 THEN '2. Mid Income ($3k-$6k)'
        ELSE '3. Low Income (< $3k)'
    END AS income_tier,
    CASE 
        WHEN debt_ratio > 0.50 THEN 'High Debt (> 50%)'
        ELSE 'Manageable Debt (<= 50%)'
    END AS debt_tier,
    COUNT(*) AS total_borrowers,
    ROUND(AVG(serious_dlq_2yrs) * 100, 2) AS default_rate_pct
FROM borrowers
GROUP BY income_tier, debt_tier
ORDER BY income_tier, debt_tier;


-- ----------------------------------------------------------------------------
-- 4. The 16-Row 3D Conduct & Leverage Stress Matrix
-- Dissects Income, Debt, and Repayment Conduct simultaneously.
-- Finding: Payment conduct strictly overpowers income volume.
-- A low-income pristine borrower (3.69% default) is 6x safer than
-- a high-earner with late marks (23.09% default).
-- ----------------------------------------------------------------------------
SELECT 
    CASE 
        WHEN monthly_income_missing = 1 THEN '4. Undisclosed Income'
        WHEN monthly_income >= 6000 THEN '1. High Income (>= $6k)'
        WHEN monthly_income >= 3000 THEN '2. Mid Income ($3k-$6k)'
        ELSE '3. Low Income (< $3k)'
    END AS income_tier,
    CASE 
        WHEN debt_ratio > 0.50 THEN 'High Debt (> 50%)'
        ELSE 'Manageable Debt (<= 50%)'
    END AS debt_tier,
    CASE 
        WHEN total_late_events = 0 THEN 'Pristine (0 Late)'
        ELSE 'Delinquent (>= 1 Late)'
    END AS payment_conduct,
    COUNT(*) AS total_borrowers,
    ROUND(AVG(serious_dlq_2yrs) * 100, 2) AS default_rate_pct
FROM borrowers
GROUP BY income_tier, debt_tier, payment_conduct
ORDER BY income_tier, debt_tier, payment_conduct;


-- ----------------------------------------------------------------------------
-- 5. Portfolio Loss Contribution & Concentration Risk (Window Function)
-- Evaluates macro loss contribution using SQL Window Functions (SUM() OVER ()).
-- Finding: Delinquent borrowers make up only 20.24% of borrowers but generate
-- 67.44% of the bank's entire default losses (Pareto concentration).
-- ----------------------------------------------------------------------------
SELECT 
    CASE 
        WHEN total_late_events = 0 THEN 'Pristine (0 Late)'
        ELSE 'Delinquent (>= 1 Late)'
    END AS payment_conduct,
    COUNT(*) AS total_borrowers,
    SUM(serious_dlq_2yrs) AS total_defaults,
    ROUND(COUNT(*) / SUM(COUNT(*)) OVER () * 100, 2) AS borrower_share_pct,
    ROUND(AVG(serious_dlq_2yrs) * 100, 2) AS default_rate_pct,
    ROUND(SUM(serious_dlq_2yrs) / SUM(SUM(serious_dlq_2yrs)) OVER () * 100, 2) AS loss_share_pct
FROM borrowers
GROUP BY payment_conduct;
