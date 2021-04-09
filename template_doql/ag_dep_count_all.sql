 /* Recursive CTEs
   Get all the affinity data for the impact charts   
				- impact report							*/
    WITH RECURSIVE impact AS ( 
    Select da1.*,
           ag.primary_device_fk, ag.name, ag.affinitygroup_pk, ag.report_type_id, ag.report_type_name, ag.last_processed ag_last_processed
    From view_affinitygroup_v2 ag
    Join view_deviceaffinity_v2 AS da1 on ag.primary_device_fk = da1.dependency_device_fk
                                      AND da1.effective_from <= ag.last_processed
                                      AND (da1.effective_to IS NULL OR da1.effective_to > current_date)
    Where ag.report_type_id = 0
    UNION 
    Select da2.*,
           dep.primary_device_fk, dep.name, dep.affinitygroup_pk, dep.report_type_id, dep.report_type_name, dep.ag_last_processed
    From impact AS dep
         Join view_deviceaffinity_v2 da2 on dep.dependent_device_fk = da2.dependency_device_fk
                                        AND da2.effective_from <= dep.ag_last_processed
                                        AND (da2.effective_to IS NULL OR da2.effective_to > current_date)
)
/* just get counts of rows per affinity group   */
	Select Distinct
		impc.affinitygroup_pk
		,impc.primary_device_fk
		,count (*) over (Partition by impc.primary_device_fk) aff_device_cnt		
	 From impact impc