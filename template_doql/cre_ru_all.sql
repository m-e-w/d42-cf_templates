WITH cre_data AS (
    SELECT
        DISTINCT device_fk
    FROM 
        view_credata_v2 
    WHERE
        recommendation_type = 'ru' AND vendor != 'VMware'
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
     (
        SELECT 
            cre_normal_aws.recommended_instance
        FROM
            view_Credata_v2 cre_normal_aws 
        WHERE 
            cre_normal_aws.vendor = 'AWS' AND cre_main.device_fk = cre_normal_aws.device_fk AND recommendation_type = 'regular'
    ) instance_normal_aws,
    cre_main.device_fk,
    CASE
        WHEN
        (
            SELECT 
                cre_normal_aws.recommended_instance
            FROM
                view_Credata_v2 cre_normal_aws 
            WHERE 
                cre_normal_aws.vendor = 'AWS' AND cre_main.device_fk = cre_normal_aws.device_fk AND recommendation_type = 'regular'
        ) = 
        (
            SELECT
                cre_aws.recommended_instance
            FROM
                view_credata_v2 cre_aws
            WHERE
                cre_aws.vendor = 'AWS' AND cre_main.device_fk = cre_aws.device_fk AND recommendation_type = 'ru'
  
        ) THEN 'True' ELSE 'False' END AS right_sized 
FROM
    cre_data cre_main

