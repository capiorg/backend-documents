from api.v1.swagger.html import get_swagger_ui_html

SWAGGER_JS_URL_STATIC = (
    "https://cdn.jsdelivr.net/npm/swagger-ui-dist@3.51.0/swagger-ui-bundle.js"
)
SWAGGER_CSS_URL_STATIC = "https://cdn.jsdelivr.net/npm/swagger-ui-dist@4/swagger-ui.css"
SWAGGER_CUSTOM_THEME_URL = (
    "https://cdn.jsdelivr.net/npm/swagger-ui-themes@3.0.1/themes/3.x/theme-material.css"
)


def custom_swagger_ui_html(*args, **kwargs):
    return get_swagger_ui_html(
        *args,
        **kwargs,
        swagger_js_url=SWAGGER_JS_URL_STATIC,
        swagger_css_url=SWAGGER_CSS_URL_STATIC,
        swagger_custom_theme_url=SWAGGER_CUSTOM_THEME_URL,
        hide_default_schemas=True
    )
