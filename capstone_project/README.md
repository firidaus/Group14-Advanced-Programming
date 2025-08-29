Tailwind setup

Run (requires Node.js):

npm install
npm run build:css

During development you can run:

npm run watch:css

This generates `core/static/css/styles.css` which is referenced from `core/templates/base.html`.

Note: Tailwind itself is installed via npm. The Python package `django-tailwind` is optional and can be used to integrate Tailwind into Django management commands.
