WITH cre_data AS (
    SELECT
        DISTINCT device_fk
    FROM 
        view_credata_v2 
    WHERE
        recommendation_type = 'ru'
)
SELECT 
    (
        SELECT
            cre_aws.recommended_instance
        FROM
            view_credata_v2 cre_aws
        WHERE
            cre_aws.vendor = 'AWS' AND cre_main.device_fk = cre_aws.device_fk AND recommendation_type = 'ru'
  
    ) instance_aws,
    (
        SELECT
            cre_azure.recommended_instance
        FROM
            view_credata_v2 cre_azure
        WHERE
            cre_azure.vendor = 'Azure' AND cre_main.device_fk = cre_azure.device_fk AND recommendation_type = 'ru'
  
    ) instance_azure,
    (
        SELECT
            cre_gcp.recommended_instance
        FROM
            view_credata_v2 cre_gcp
        WHERE
            cre_gcp.vendor = 'GCP' AND cre_main.device_fk = cre_gcp.device_fk AND recommendation_type = 'ru'
  
    ) instance_gcp,
    cre_main.device_fk
FROM
    cre_data cre_main

