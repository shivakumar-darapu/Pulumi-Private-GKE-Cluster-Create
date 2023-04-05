import pulumi
import pulumi_gcp as gcp


class Custom_Gcp_Network:

    def __init__(self, vpc_name, subnet_info):
        self.vpc_name = vpc_name
        self.subnet_info = subnet_info
        self.subnets = []
        self.vpc_network = None
    def create_network(self):
        self.vpc_network = gcp.compute.Network(resource_name=self.vpc_name,
                                          auto_create_subnetworks=False,
                                          name=self.vpc_name)
        vpc_id = self.vpc_network.id
        for subnet in self.subnet_info:
            self.subnets.append(gcp.compute.Subnetwork(resource_name=subnet["subnet_name"],
                                                       ip_cidr_range=subnet["subnet_cidr"],
                                                       region=subnet["subnet_region"],
                                                       name=subnet["subnet_name"],
                                                       network=vpc_id))


class Custom_Gcp_Cluster:

    def __init__(self, cluster_info, vpc_id, subnet_info):
        self.subnets = subnet_info
        self.cluster_info = cluster_info
        self.vpc_id = vpc_id
        self.networks = []
        self.k8s_cluster = None
        
    # def create_backup_plan(self, backup_plan_config, project):
    #     for backup_config in backup_plan_config:
    #         backup_plan = gcp.gkebackup.BackupPlan(name=backup_config["backup_plan_name"],
    #                     project=project,
    #                     cluster=backup_config["cluster_name"],
    #                     location=backup_config["backup_location"],
    #                     deactivated=backup_config[""],
    #                     backup_config=gcp.gkebackup.BackupPlanBackupConfigArgs(
    #                         include_volume_data=backup_config["backup_volume_data"],
    #                         include_secrets=backup_config[""],
    #                         selected_namespaces=gcp.gkebackup.BackupPlanBackupConfigSelectedNamespacesArgs(
    #                             namespaces=[
    #                                 "default",
    #                                 "test",
    #                             ],
    #                         ),
    #                         encryption_key=gcp.gkebackup.BackupPlanBackupConfigEncryptionKeyArgs(
    #                             gcp_kms_encryption_key=crypto_key.id,
    #                         ),
    #                     )
    #                 )
        
    def create_container_registery(self,name, project, location):
        registry = gcp.container.Registry(name,
                                        location=location,
                                        project=project)
    
    def create_custom_cluster(self):
        for counter_outer_loop in range(len(self.cluster_info)):
            cluster = self.cluster_info[counter_outer_loop]
            self.k8s_cluster = gcp.container.Cluster(resource_name=cluster["cluster_name"],
                                                name=cluster["cluster_name"],
                                                initial_node_count=1,
                                                networking_mode="VPC_NATIVE",  # Required For Having nodes Private
                                                ip_allocation_policy=gcp.container.ClusterIpAllocationPolicyArgs(
                                                    # Required for having the Cluster private
                                                    cluster_ipv4_cidr_block=cluster["cluster_cidr"],
                                                    services_ipv4_cidr_block=cluster["services_cidr"]
                                                ),
                                                location=cluster["location"],
                                                subnetwork=self.subnets[counter_outer_loop].id,
                                                network=cluster["network"],
                                                min_master_version=cluster["master_version"],
                                                remove_default_node_pool=True,
                                                node_config=gcp.container.ClusterNodeConfigArgs(
                                                    machine_type="e2-medium"),
                                                workload_identity_config=gcp.container.ClusterWorkloadIdentityConfigArgs(
                                                    workload_pool=cluster["workload_pool"]
                                                ),
                                                master_authorized_networks_config=gcp.container.ClusterMasterAuthorizedNetworksConfigArgs(
                                                    # Required for having the Cluster private
                                                    cidr_blocks=cluster["authorizednetworks"],
                                                    gcp_public_cidrs_access_enabled=False,
                                                ),
                                                private_cluster_config=gcp.container.ClusterPrivateClusterConfigArgs(
                                                    # Required for having the Cluster private
                                                    enable_private_nodes=cluster["enable_private_nodes"],
                                                    enable_private_endpoint=cluster["enable_private_endpoint"],
                                                    master_ipv4_cidr_block=cluster["master_cidr"],
                                                    master_global_access_config=gcp.container.ClusterPrivateClusterConfigMasterGlobalAccessConfigArgs(
                                                        enabled=True
                                                    )
                                                ),
                                                monitoring_config=gcp.container.ClusterMonitoringConfigArgs(
                                                    enable_components = cluster["monitor_components"],
                                                    managed_prometheus = gcp.container.ClusterMonitoringConfigManagedPrometheusArgs(
                                                        enabled=cluster["enable_prometheus"]
                                                        )
                                                    ),
                                                addons_config=gcp.container.ClusterAddonsConfigArgs(
                                                    gke_backup_agent_config=gcp.container.ClusterAddonsConfigGkeBackupAgentConfigArgs(
                                                        enabled=cluster["enable_gke_backups"]
                                                    )
                                                )
                                                )
            for node in cluster["node_info"]:
                node_pool = gcp.container.NodePool(cluster=self.k8s_cluster.name,
                                                   resource_name=node["node_pool_name"],
                                                   location=cluster["location"],
                                                   name=node["node_pool_name"],
                                                   node_config=gcp.container.NodePoolNodeConfigArgs(
                                                       machine_type=node["machine_type"],
                                                       disk_size_gb=node["machine_disk_size"],
                                                       disk_type=node["machine_disk_type"],
                                                       # pd-standard, pd-balanced, pd-ssd
                                                       image_type=node["machine_image_type"],
                                                       # cos_containerd, cos, ubuntu_containerd
                                                       preemptible=node["preemptible_machines"]
                                                   ),
                                                   node_count=node["node_count"],
                                                   node_locations=node["node_locations"],
                                                   version=node["node_version"])

    def create_nat_gateway(self, nat_info):
        
        for nat in nat_info:
            router = gcp.compute.Router(nat["router_name"],
                region=nat["subnet_region"],
                network=nat["network_name"]
            )
            nat_gtw = gcp.compute.RouterNat(nat["Nat_gateway_name"],
                router=router.name,
                region=router.region,
                nat_ip_allocate_option="AUTO_ONLY",
                source_subnetwork_ip_ranges_to_nat="ALL_SUBNETWORKS_ALL_IP_RANGES",
                log_config=gcp.compute.RouterNatLogConfigArgs(
                    enable=True,
                    filter="ERRORS_ONLY",
                )
            )