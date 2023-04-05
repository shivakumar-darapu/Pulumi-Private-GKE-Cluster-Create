"""A Google Cloud Python Pulumi program"""

from pulumi import ResourceOptions
import Variables as var
import GCP 

# Check On which cloud the cluster needs to be created
if var.preferred_cloud.upper() == "GCP":
    if var.create_network == True:
        my_custom_network = GCP.Custom_Gcp_Network(vpc_name=var.vpc_name, subnet_info=var.subnet_info)
        my_custom_network.create_network()
        
    if var.create_cluster == True:
        my_k8s_cluster = GCP.Custom_Gcp_Cluster(var.cluster_info , my_custom_network.vpc_network.id, my_custom_network.subnets)
        my_k8s_cluster.create_custom_cluster()
        my_k8s_cluster.create_nat_gateway(var.gateway_info)
        
    if var.create_container_register == True:
        my_k8s_cluster.create_container_registery(name=var.registery_name, project=var.project, location=var.location)
    
    if var.create_backup_plan == True:
        my_k8s_cluster.create_backup_plan()
        
elif var.preferred_cloud.upper() == "AZURE":
    print(" Creating Cluster in Azure ")
elif var.preferred_cloud.upper() == "AWS":
    print(" Creating Cluster in AWS ")
else:
    print("Your Selected Cloud is Currently Not Supported!!! ")
