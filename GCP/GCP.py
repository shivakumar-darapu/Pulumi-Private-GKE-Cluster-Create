import pulumi
import pulumi_gcp as gcp


class Custom_Gcp_Network:

    def __init__(self, vpc_name, subnet_info):
        self.vpc_name = vpc_name
        self.subnet_info = subnet_info

    def create_network(self):
        vpc_network = gcp.compute.Network(resource_name=self.vpc_name,
                                          auto_create_subnetworks=False,
                                          name=self.vpc_name)

        subnets = []  # This will store the subnet output object
        for subnet in self.subnet_info:
            subnets.append(gcp.compute.Subnetwork(resource_name=subnet["subnet_name"],
                                                  ip_cidr_range=subnet["subnet_cidr"],
                                                  region=subnet["subnet_region"],
                                                  name=subnet["subnet_name"],
                                                  network=vpc_network.id))
