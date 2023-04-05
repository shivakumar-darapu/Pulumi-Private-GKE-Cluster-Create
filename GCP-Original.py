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
    
    def create_public_cluster(self):
        print(f"subnet info {self.subnets}")
        for counter_outer_loop in range(len(self.cluster_info)):
            cluster = self.cluster_info[counter_outer_loop]
            print(f"cluster details : {cluster}")
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

    def create_private_cluster(self):
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
                                                    gcp_public_cidrs_access_enabled=False
                                                ),
                                                private_cluster_config=gcp.container.ClusterPrivateClusterConfigArgs(
                                                    # Required for having the Cluster private
                                                    enable_private_nodes=cluster["enable_private_nodes"],
                                                    enable_private_endpoint=cluster["enable_private_endpoint"],
                                                    master_ipv4_cidr_block=cluster["master_cidr"],
                                                    master_global_access_config=gcp.container.ClusterPrivateClusterConfigMasterGlobalAccessConfigArgs(
                                                        enabled=cluster["enable_private_endpoint"]
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
                                                       disk_type=node["machine_disk_type"],# pd-standard, pd-balanced, pd-ssd
                                                       image_type=node["machine_image_type"],# cos_containerd, cos, ubuntu_containerd
                                                       preemptible=node["preemptible_machines"]
                                                   ),
                                                   node_count=node["node_count"],
                                                   node_locations=node["node_locations"],
                                                   version=node["node_version"])
