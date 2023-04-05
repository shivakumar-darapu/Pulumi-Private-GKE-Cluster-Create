# **************************  Cloud ******************************
preferred_cloud = "GCP"  # GCP / AZURE / AWS
# ****************************************************************

# ************************* CONTAINER REGISTERY *********************
create_container_register = True,
registery_name = "my-test-registery"
project = "warm-tokenizer-376310",
location = "US",

# ****************************************************************
# ************************* CONTAINER REGISTERY *********************
create_backup_plan = True,
backup_plan_config = [
    {   
        "cluster_name": "gke-cluster",
        "backup_plan_name": "my_test_backup_plan",
        "backup_location": "us-central1",
        "backup_volume_data": True,
        "backup_secrets": True,
        "backup_only_selected_applications": True,
        "selected_applications":[
                {
                    "name": "",
                    "namespace:": ""
                }
            
            ], # List of namespaced names 
        "backup_only_selected_applications": False, # Either only selected apps or all apps in selected namespaces
        "selected_namespaces": ["default"],
        "backup_plan_deactivate": False,
        "backup_schedule": {
            "cron_schedule": "0/7 0 0 ? * SAT *",
            "paused": False
        },
        "backup_retain_days": 7
        
    }
    ]
# ****************************************************************
# ************************* NETWORK CREATION *********************

create_network = True  # --> Provide a bool value if the network needs to be created <--
vpc_name = "my-test-network"
subnet_info = [
    {
        "subnet_name": "us-central1-subnet",
        "subnet_region": "us-central1",
        "subnet_cidr": "172.1.0.0/24"
    },
    {
        "subnet_name": "us-west1-subnet",
        "subnet_region": "us-west1",
        "subnet_cidr": "172.2.0.0/24"
    }
]

# ****************************************************************

# ************************* CLUSTER CREATION *********************
create_cluster = True  # --> Provide a bool value if the Cluster needs to be created <--
cluster_info = [
    {
        "cluster_name": "gke-cluster",
        "location": "us-central1-c",
        "min_master_version": "1.24.10-gke.2300",
        "master_version": "1.24.10-gke.2300",
        "network": "my-test-network",
        "subnet": "us-central1-subnet",
        "networking_mode": "VPC_NATIVE",  # Allowed Values --> VPC_NATIVE / ROUTES
        "enable_gke_backups": True,
        # If You need a Private Cluster provide below details
        "enable_private_endpoint": False,  # Make your Cluster Accessible only on private ip --> ** True For Private Endpoint **
        "enable_private_nodes": True,  # Make your Vm's in node pool private
        "master_cidr": "172.16.0.0/28",
        "cluster_cidr": "192.168.0.0/21",
        "services_cidr": "192.168.9.0/24",
        "monitor_components": ["SYSTEM_COMPONENTS", "APISERVER", "CONTROLLER_MANAGER", "SCHEDULER"],
        "enable_prometheus": False,
        "workload_pool": "warm-tokenizer-376310.svc.id.goog", # PROJECT_ID.svc.id.goog
        "authorizednetworks": [
            {
                "cidr_block": "192.168.1.0/24",
                "display_name": "myenv"
            }
            # {
            #     "cidr_block": "165.225.121.39/32",
            #     "display_name": "myip"
            # }
        ],
        "node_info": [
            {
                "node_pool_name": "dev",
                "node_count": 1,
                "node_version": "1.24.10-gke.2300",
                "node_locations": ["us-central1-c"],  # Specify a list of zones in case of regional
                "machine_type": "e2-medium",
                "machine_image_type": "cos_containerd",  # cos_containerd, cos, ubuntu_containerd
                "machine_disk_type": "pd-standard",  # pd-standard, pd-balanced, pd-ssd
                "machine_disk_size": 10,
                "preemptible_machines": False
            }
        ]
    }
]

# ****************************************************************
# ************************* NAT GATEWAY *************************

gateway_info = [
    {
        "router_name": "test-router",
        "subnet_region": "us-central1",
        "network_name": "my-test-network",
        "Nat_gateway_name": "test-nat"
    }
]

# ****************************************************************