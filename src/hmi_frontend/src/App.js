import React from 'react';
import {BrowserRouter as Router, Route, Routes} from 'react-router-dom';
import SearchByTimestamp from './SearchByTimestamp';
import ResultsPage from './ResultsPage';
import './App.css';

function App() {
    return (
        <div className="App">
            <h1>Human Machine Interface</h1>
            <Router>
                <Routes>
                    <Route path="/" element={<SearchByTimestamp />} />
                    <Route path="/results" element={<ResultsPage />} />
                </Routes>
            </Router>
        </div>
    );
}

export default App;
