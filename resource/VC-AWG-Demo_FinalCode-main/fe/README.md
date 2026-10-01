# Financial Management Frontend

The frontend application is built with React + TypeScript + Vite + TailwindCSS.

## 🚀 Installation

```bash
# Install dependencies
npm install

# Run the development server
npm run dev

# Build production
npm run build

# Preview production build
npm run preview
```

## 📁 Directory structure

```
src/
 ├── api/            # Axios instance and service functions
 ├── assets/         # Images, icons
 ├── components/     # Reusable components
 ├── context/        # React Context (Auth, Theme)
 ├── hooks/          # Custom hooks
 ├── pages/          # Main pages
 ├── router/         # Route definitions
 ├── utils/          # Helper functions
 ├── App.tsx
 └── main.tsx
```

## 🔧 Environment configuration

Create an `.env` file in the `fe/` directory:

```
VITE_API_BASE_URL=http://localhost:8000/api
```

## 📦 Main dependencies

- **React 18** - UI library
- **TypeScript** - Type safety
- **Vite** - Build tool
- **React Router v6** - Routing
- **Axios** - HTTP client
- **TailwindCSS** - Styling
- **Zustand** - State management (optional)

## 🎨 UI Components

- `Button` - Button component with multiple variants
- `Input` - Input component with validation
- `Loading` - Loading spinner
- `Error` - Error display component
- `Layout` - Main layout with a header and footer

## 🔐 Authentication

The application uses a JWT token stored in localStorage. The Context API is used to manage authentication state.

## 🌙 Theme

Dark mode is supported through ThemeContext. The theme is stored in localStorage.
