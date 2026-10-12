import { createRoot } from 'react-dom/client';
import Clinic from './App';
import '@fontsource/poppins/400.css';
import '@fontsource/poppins/500.css';
import '@fontsource/poppins/600.css';
import '@fontsource/poppins/700.css';
import './clinic.css';
createRoot(document.getElementById('root')!).render(<Clinic />);
