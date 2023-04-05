import pulumi
import pulumi_gcp as gcp


class Gcp_Cluster:
    networks = []
    clusters = []
    k8s_cluster = []

    def __init__(self, cluster_info):
        self.cluster_info = cluster_info

    def create_public_cluster(self):
        for cluster in self.cluster_info:
            k8s_cluster = gcp.container.Cluster(resource_name=cluster["cluster_name"],
                                                name=cluster["cluster_name"],
                                                initial_node_count=1,
                                                networking_mode="VPC_NATIVE",
                                                location=cluster["location"],
                                                subnetwork=cluster["subnet"],
                                                network=cluster["network"],
                                                node_config=gcp.container.ClusterNodeConfigArgs(
                                                    machine_type="e2-medium"),
                                                addons_config=gcp.container.ClusterAddonsConfigArgs(
                                                    gke_backup_agent_config=gcp.container.ClusterAddonsConfigGkeBackupAgentConfigArgs(
                                                        enabled=cluster["enable_gke_backups"]
                                                    )
                                                ))
            for node in self.cluster_info["node_info"]:
                node_pool = gcp.container.NodePool(cluster=k8s_cluster.name,
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

    def create_private_cluster(self):
        for cluster in self.cluster_info:
            k8s_cluster = gcp.container.Cluster(resource_name=cluster["cluster_name"],
                                                name=cluster["cluster_name"],
                                                initial_node_count=1,
                                                networking_mode="VPC_NATIVE",  # Required For Having nodes Private
                                                ip_allocation_policy=gcp.container.ClusterIpAllocationPolicyArgs(
                                                    # Required for having the Cluster private
                                                    cluster_ipv4_cidr_block=cluster["cluster_cidr"],
                                                    services_ipv4_cidr_block=cluster["services_cidr"]
                                                ),
                                                location=cluster["location"],
                                                subnetwork=cluster["subnet"],
                                                network=cluster["network"],
                                                min_master_version=cluster["1.22.15-gke.2500"],
                                                remove_default_node_pool=True,
                                                node_config=gcp.container.ClusterNodeConfigArgs(
                                                    machine_type="e2-medium"),
                                                workload_identity_config=gcp.container.ClusterWorkloadIdentityConfigArgs(
                                                    workload_pool=cluster["workload_pool"]
                                                ),
                                                master_authorized_networks_config=gcp.container.ClusterMasterAuthorizedNetworksConfigArgs(
                                                    # Required for having the Cluster private
                                                    # cidr_blocks=gcp.container.ClusterMasterAuthorizedNetworksConfigCidrBlockArgs(),
                                                    gcp_public_cidrs_access_enabled=cluster["enable_private_endpoint"],
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
            for node in self.cluster_info["node_info"]:
                node_pool = gcp.container.NodePool(cluster=k8s_cluster.name,
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
