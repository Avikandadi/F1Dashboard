# F1 Dashboard - Frontend

A modern React frontend for the F1 Results & Predictions dashboard.

## Features

- **Dashboard Home**: Overview of recent races and championship standings
- **Race Explorer**: Browse historical race data with interactive charts
- **AI Predictions**: Generate ML-powered predictions for upcoming races
- **Responsive Design**: Optimized for desktop and mobile devices
- **Real-time Data**: Live data from the FastAPI backend

## Tech Stack

- **React 18** - Modern React with hooks
- **TypeScript** - Type-safe JavaScript
- **Vite** - Fast build tool and dev server  
- **Tailwind CSS** - Utility-first CSS framework
- **React Router** - Client-side routing
- **Recharts** - Chart and visualization library
- **Axios** - HTTP client for API calls
- **Lucide React** - Beautiful icon library

## Getting Started

### Prerequisites

- Node.js 18+ and npm (or yarn/pnpm)
- Backend API running on `http://localhost:8000`

### Installation

1. **Navigate to the frontend directory**:
   ```bash
   cd frontend
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Start the development server**:
   ```bash
   npm run dev
   ```

4. **Open your browser**: `http://localhost:5173`

## Available Scripts

- `npm run dev` - Start development server with hot reload
- `npm run build` - Build for production
- `npm run preview` - Preview production build locally
- `npm run lint` - Run ESLint for code quality

## Project Structure

```
frontend/
├── public/                 # Static assets
├── src/
│   ├── components/        # Reusable UI components
│   │   ├── Navbar.tsx     # Navigation bar
│   │   ├── Card.tsx       # Card container
│   │   ├── Table.tsx      # Data table
│   │   └── LineChart.tsx  # Chart component
│   ├── pages/            # Page components
│   │   ├── Home.tsx      # Dashboard home
│   │   ├── RaceExplorer.tsx # Race data browser
│   │   ├── Predictions.tsx  # AI predictions
│   │   └── Compare.tsx   # Driver comparison (coming soon)
│   ├── lib/
│   │   └── api.ts        # API client and functions
│   ├── types.ts          # TypeScript type definitions
│   ├── App.tsx           # Main app component
│   ├── main.tsx         # React entry point
│   └── index.css        # Global styles (Tailwind)
├── index.html            # HTML template
├── package.json          # Dependencies and scripts
├── tailwind.config.js    # Tailwind configuration
├── tsconfig.json        # TypeScript configuration
├── vite.config.ts       # Vite configuration
└── README.md            # This file
```

## API Integration

The frontend connects to the backend API for all data:

- **Base URL**: `http://localhost:8000/api`
- **Health Check**: `http://localhost:8000/health`
- **CORS**: Configured for `http://localhost:5173`

### API Client

The `src/lib/api.ts` file contains all API interaction logic:

```typescript
import { f1Api } from './lib/api'

// Get races for a season
const races = await f1Api.getRaces(2024)

// Generate predictions
const prediction = await f1Api.predict({
  season: 2024,
  round: 1,
  session_type: 'qualifying'
})
```

## Styling

The app uses Tailwind CSS with a custom F1-themed color palette:

```css
colors: {
  f1: {
    red: '#FF1801',    /* F1 red */
    dark: '#15151E',   /* Dark background */
    gray: '#38383F',   /* Card background */
    light: '#F7F4F4',  /* Light text */
  }
}
```

## Development

### Adding New Components

1. Create component in `src/components/`
2. Export from component file
3. Import and use in pages or other components

### Adding New Pages

1. Create page component in `src/pages/`
2. Add route in `App.tsx`
3. Add navigation link in `Navbar.tsx`

### API Integration

1. Add new API function in `src/lib/api.ts`
2. Define TypeScript types in `src/types.ts`
3. Use in components with proper error handling

## Deployment

### Build for Production

```bash
npm run build
```

The build artifacts will be stored in the `dist/` directory.

### Environment Variables

For production, update the API base URL in `src/lib/api.ts`:

```typescript
const API_BASE_URL = process.env.VITE_API_URL || 'http://localhost:8000/api'
```

## Troubleshooting

### Common Issues

1. **API connection errors**: 
   - Ensure backend is running on `http://localhost:8000`
   - Check CORS configuration
   - Verify API endpoints in browser dev tools

2. **Build errors**:
   - Clear node_modules: `rm -rf node_modules && npm install`
   - Check TypeScript errors: `npm run build`

3. **Styling issues**:
   - Verify Tailwind classes are correct
   - Check if custom F1 colors are defined in `tailwind.config.js`

### Performance Optimization

- Components use React hooks for state management
- API calls are cached where appropriate
- Charts are optimized for performance with data sampling
- Images and assets are optimized

## Browser Support

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## Contributing

1. Follow the existing code style
2. Add TypeScript types for new features
3. Test components in different screen sizes
4. Update documentation for new features

## License

This project is for educational and demonstration purposes.
