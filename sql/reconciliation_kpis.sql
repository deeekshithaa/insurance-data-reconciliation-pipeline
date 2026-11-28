-- Insurance Policy Reconciliation KPIs

-- 1. Total policy records and reconciliation outcomes
SELECT
    COUNT(*) AS total_policies,
    COUNT(*) FILTER (WHERE match_status = 'Matched') AS matched_policies,
    COUNT(*) FILTER (WHERE match_status = 'Missing from Agency A') AS missing_from_agency_a,
    COUNT(*) FILTER (WHERE match_status = 'Missing from Agency B') AS missing_from_agency_b
FROM public.fact_policy;


-- 2. Discrepancy KPIs
SELECT
    COUNT(*) FILTER (WHERE premium_mismatch = TRUE) AS premium_mismatches,
    COUNT(*) FILTER (WHERE customer_name_mismatch = TRUE) AS customer_name_mismatches,
    COUNT(*) FILTER (WHERE has_discrepancy = TRUE) AS policies_with_discrepancies
FROM public.fact_policy;


-- 3. Premium discrepancy impact
SELECT
    COUNT(*) AS premium_mismatch_count,
    SUM(ABS(premium_difference)) AS total_premium_difference,
    AVG(ABS(premium_difference)) AS average_premium_difference
FROM public.fact_policy
WHERE premium_mismatch = TRUE;