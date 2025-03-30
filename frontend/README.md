# Fixrify Frontend

This is the frontend application for Fixrify, a home repair and maintenance service platform built with Vue.js.

## Features

- User authentication (login/register)
- Service browsing and booking
- User dashboard with booking management
- Admin dashboard for service and user management
- Responsive design with Bootstrap 5
- State management with Vuex
- API integration with Axios

## Prerequisites

- Node.js (v14 or higher)
- npm (v6 or higher)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/fixrify.git
cd fixrify/frontend
```

2. Install dependencies:
```bash
npm install
```

3. Create a `.env` file in the root directory and add the following:
```
VUE_APP_API_URL=http://localhost:5000
VUE_APP_TITLE=Fixrify
```

## Development

To start the development server:

```bash
npm run serve
```

The application will be available at `http://localhost:8080`.

## Building for Production

To build the application for production:

```bash
npm run build
```

The built files will be in the `dist` directory.

## Project Structure

```
frontend/
├── public/
├── src/
│   ├── assets/
│   ├── components/
│   ├── router/
│   ├── store/
│   ├── views/
│   ├── App.vue
│   └── main.js
├── .env
├── .gitignore
├── package.json
└── README.md
```

## Technologies Used

- Vue.js 3
- Vue Router
- Vuex
- Bootstrap 5
- Axios
- Font Awesome

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 