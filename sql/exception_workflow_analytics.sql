-- 1. Exception backlog by priority and workflow status
SELECT
    priority,
    review_status,
    COUNT(*) AS exception_count
FROM public.exception_management
GROUP BY priority, review_status
ORDER BY priority, review_status;


-- 2. Exception resolution performance by priority
SELECT
    priority,
    COUNT(*) AS total_exceptions,
    COUNT(*) FILTER (WHERE review_status = 'Open') AS open_exceptions,
    COUNT(*) FILTER (WHERE review_status = 'Resolved') AS resolved_exceptions,
    ROUND(
        100.0 * COUNT(*) FILTER (WHERE review_status = 'Resolved')
        / COUNT(*),
        2
    ) AS resolution_rate_pct
FROM public.exception_management
GROUP BY priority
ORDER BY priority;