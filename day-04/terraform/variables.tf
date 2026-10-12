variable "project_name" {
  description = "Name used to identify ProductionOps resources"
  type        = string
  default     = "productionops"
}

variable "instance_type" {
  description = "EC2 instance type for the ProductionOps lab"
  type        = string
  default     = "t3.micro"
}
