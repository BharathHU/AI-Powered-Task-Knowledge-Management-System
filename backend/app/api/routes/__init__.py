# Package: app.api.routes
# Exposes all API route modules so they can be discovered by the main app.
# Each module maps to a logical domain: auth, tasks, documents, search, analytics.

from app.api.routes import analytics, auth, documents, search, tasks
