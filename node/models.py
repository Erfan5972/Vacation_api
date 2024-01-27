from django.db import models


class Node(models.Model):
    name = models.CharField(max_length=300)
    is_final = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class NodeConnection(models.Model):
    from_node = models.ForeignKey(Node, on_delete=models.CASCADE, related_name='Node_NodeConnection1')
    to_node = models.ForeignKey(Node, on_delete=models.CASCADE, related_name='Node_NodeConnection2')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.from_node}//{self.to_node}"