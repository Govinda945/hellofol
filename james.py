
val='{\n"aws_instance" = {\n"example" = {\n"instance_type" = "t2.micro"\n"ami" = "ami-abc123"\n}\n\n}\n\n}\n'
# print('{\n"aws_instance" = {\n"example" = {\n"instance_type" = "t2.micro"\n"ami" = "ami-abc123"\n}\n\n}\n\n}\n')
print(val.split('{\n'))