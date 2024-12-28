class RobotsHeaderMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Set 'X-Robots-Tag' for specific URLs (like /sitemap.xml)
        if request.path == '/sitemap.xml':
            response['X-Robots-Tag'] = "index, follow"  # or "noindex, nofollow" depending on your need

        return response
