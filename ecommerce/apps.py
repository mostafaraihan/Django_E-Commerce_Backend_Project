from django.apps import AppConfig


class EcommerceConfig(AppConfig):
    name = 'ecommerce'

class PollsConfig(AppConfig):
    name = 'polls'
    icon = 'fa fa-square-poll-vertical'  # FontAwesome icon
    divider_title = "Apps"  # Section divider title
    priority = 0  # Sidebar ordering (higher = top)
    hide = False  # Hide from sidebar