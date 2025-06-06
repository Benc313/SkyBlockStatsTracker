import React, { useState, useEffect, useCallback, useMemo } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { format } from 'date-fns';

// --- Helper Functions & Configuration ---

const API_BASE_URL = 'http://127.0.0.1:5000';

const NAME_MAP = {
    'total_money': 'Total Money', // For the history chart legend
    'kills': 'Total Kills',
    'deaths': 'Total Deaths',
};

// --- Reusable UI Components ---

const Card = ({ title, children, className = '' }) => (
    <div className={`bg-gray-800/50 border border-gray-700/50 rounded-xl p-6 shadow-2xl flex flex-col backdrop-blur-sm ${className}`}>
        <h2 className="text-xl font-bold text-white mb-4 pb-3 border-b border-gray-700">{title}</h2>
        {children}
    </div>
);

const StatBox = ({ label, value, colorClass = 'text-indigo-400' }) => (
    <div className="text-center">
        <p className="text-sm text-gray-400 uppercase tracking-wider font-semibold">{label}</p>
        <p className={`text-4xl font-bold tracking-tighter ${colorClass}`}>{value}</p>
    </div>
);

const TimeRangeSelector = ({ onSelect, activeRange, ranges = ['today', '7d', '30d'] }) => (
    <div className="flex justify-end gap-2 mb-4">
        {ranges.map(range => (
            <button
                key={range}
                onClick={() => onSelect(range)}
                className={`px-3 py-1 text-sm font-semibold rounded-md transition-all duration-200 ${
                    activeRange === range
                        ? 'bg-indigo-500 text-white shadow-lg'
                        : 'bg-gray-700/50 text-gray-300 hover:bg-gray-600/50'
                }`}
            >
                {range.charAt(0).toUpperCase() + range.slice(1)}
            </button>
        ))}
    </div>
);

const MultiSelectFilter = ({ items, selectedItems, onSelectionChange, formatName }) => {
    return (
        <div className="flex flex-wrap gap-2 mb-4">
            {items.map(item => (
                <button
                    key={item}
                    onClick={() => onSelectionChange(item)}
                    className={`px-3 py-1 text-xs font-semibold rounded-full transition-all duration-200 ${
                        selectedItems.includes(item)
                            ? 'bg-indigo-500 text-white'
                            : 'bg-gray-700/50 text-gray-300 hover:bg-gray-600/50'
                    }`}
                >
                    {formatName(item)}
                </button>
            ))}
        </div>
    );
};

const LoadingSpinner = () => (
    <div className="absolute inset-0 flex items-center justify-center text-gray-400 bg-gray-800/50 rounded-lg">
        <svg className="animate-spin h-8 w-8 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
        </svg>
    </div>
);

// --- Data-driven Components ---

function LatestStats() {
    const [stats, setStats] = useState(null);

    useEffect(() => {
        const fetchLatestStats = async () => {
            try {
                const tsRes = await fetch(`${API_BASE_URL}/api/latest_snapshot_timestamp`);
                const tsData = await tsRes.json();
                if (tsData.latest_timestamp) {
                    const statsRes = await fetch(`${API_BASE_URL}/api/profile_stats/${tsData.latest_timestamp}`);
                    const statsData = await statsRes.json();
                    setStats(statsData);
                }
            } catch (error) {
                console.error("Failed to fetch latest stats:", error);
            }
        };
        fetchLatestStats();
    }, []);

    const totalMoney = useMemo(() => {
        if (!stats) return '...';
        const combined = (stats.purse || 0) + (stats.bank_balance || 0);
        return Math.round(combined).toLocaleString();
    }, [stats]);

    return (
        <Card title="Latest Profile Stats">
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
                <StatBox label="Total Money" value={totalMoney} colorClass="text-green-400" />
                <StatBox label="Total Kills" value={stats ? stats.kills.toLocaleString() : '...'} colorClass="text-red-400" />
                <StatBox label="Total Deaths" value={stats ? stats.death_count.toLocaleString() : '...'} colorClass="text-gray-500" />
            </div>
        </Card>
    );
}

function ProgressTable({ title, apiEndpoint }) {
    const [data, setData] = useState([]);
    const [loading, setLoading] = useState(true);
    const [timeRange, setTimeRange] = useState('today');

    const fetchData = useCallback(async () => {
        setLoading(true);
        try {
            const res = await fetch(`${API_BASE_URL}/api/diff/${apiEndpoint}?range=${timeRange}`);
            const progressData = await res.json();
            setData(progressData);
        } catch (error) {
            console.error(`Failed to fetch ${title} progress:`, error);
        } finally {
            setLoading(false);
        }
    }, [apiEndpoint, timeRange, title]);

    useEffect(() => {
        fetchData();
    }, [fetchData]);

    const formatName = (name) => name.replace(/_/g, ' ').replace(/:/g, ' ').replace(/\b\w/g, l => l.toUpperCase());

    return (
        <Card title={title}>
            <TimeRangeSelector onSelect={setTimeRange} activeRange={timeRange} />
            <div className="flex-grow overflow-y-auto h-80 relative">
                {loading && <LoadingSpinner />}
                {!loading && data.length === 0 && (
                    <div className="absolute inset-0 flex items-center justify-center text-gray-400">No progress in this period.</div>
                )}
                {!loading && data.length > 0 && (
                     <table className="w-full text-sm text-left">
                        <thead className="text-xs text-gray-400 uppercase bg-gray-800 sticky top-0">
                            <tr>
                                <th scope="col" className="px-4 py-2">Item</th>
                                <th scope="col" className="px-4 py-2 text-right">Progress</th>
                                <th scope="col" className="px-4 py-2 text-right">Total</th>
                            </tr>
                        </thead>
                        <tbody>
                            {data.map(item => (
                                <tr key={item.name} className="border-b border-gray-700 hover:bg-gray-700/50">
                                    <td className="px-4 py-2 font-medium text-white whitespace-nowrap">{formatName(item.name)}</td>
                                    <td className="px-4 py-2 text-green-400 font-semibold text-right">+{item.progress.toLocaleString()}</td>
                                    <td className="px-4 py-2 text-gray-400 text-right">{item.end_value.toLocaleString()}</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                )}
            </div>
        </Card>
    );
}

function HistoricalChart({ title, apiEndpoint }) {
    const [loading, setLoading] = useState(true);
    const [timeRange, setTimeRange] = useState('7d');
    const [allItems, setAllItems] = useState([]);
    const [selectedItems, setSelectedItems] = useState([]);
    const [chartData, setChartData] = useState([]);

    const formatName = (name) => (NAME_MAP[name] || name).replace(/_/g, ' ').replace(/:/g, ' ').replace(/\b\w/g, l => l.toUpperCase());

    const fetchData = useCallback(async () => {
        setLoading(true);
        try {
            const res = await fetch(`${API_BASE_URL}/api/history/${apiEndpoint}?range=${timeRange}`);
            const historyData = await res.json();
            
            const itemKeys = Object.keys(historyData);
            setAllItems(itemKeys);

            if (selectedItems.length === 0 && itemKeys.length > 0) {
                 const sortedItems = itemKeys.sort((a, b) => {
                    const lastA = historyData[a][historyData[a].length - 1]?.value || 0;
                    const lastB = historyData[b][historyData[b].length - 1]?.value || 0;
                    return lastB - lastA;
                });
                setSelectedItems(sortedItems.slice(0, 5));
            }

            const reformattedData = {};
            for (const key in historyData) {
                historyData[key].forEach(point => {
                    const date = format(new Date(point.timestamp * 1000), 'yyyy-MM-dd');
                    if (!reformattedData[date]) reformattedData[date] = { date };
                    reformattedData[date][key] = point.value;
                });
            }
            setChartData(Object.values(reformattedData).sort((a, b) => new Date(a.date) - new Date(b.date)));
        } catch (error) {
            console.error(`Failed to fetch ${title} history:`, error);
        } finally {
            setLoading(false);
        }
    }, [apiEndpoint, timeRange, title, selectedItems.length]);

    useEffect(() => {
        fetchData();
    }, [fetchData]);

    const handleFilterChange = (item) => {
        setSelectedItems(prev => 
            prev.includes(item) ? prev.filter(i => i !== item) : [...prev, item]
        );
    };
    
    const COLORS = ['#8884d8', '#82ca9d', '#ffc658', '#ff7300', '#00C49F', '#FFBB28', '#FF8042', '#0088FE', '#ff80ea', '#d65c8d'];

    return (
        <Card title={title}>
            <div className="flex justify-between items-start">
                <MultiSelectFilter items={allItems} selectedItems={selectedItems} onSelectionChange={handleFilterChange} formatName={formatName} />
                <TimeRangeSelector onSelect={setTimeRange} activeRange={timeRange} ranges={['7d', '30d', 'all']} />
            </div>
            <div className="flex-grow relative h-[400px]">
                {loading && <LoadingSpinner />}
                {!loading && (
                    <ResponsiveContainer width="100%" height="100%">
                        <LineChart data={chartData} margin={{ top: 5, right: 20, left: 10, bottom: 5 }}>
                            <CartesianGrid strokeDasharray="3 3" stroke="#4a5568" />
                            <XAxis dataKey="date" tick={{ fill: '#a0aec0' }} tickFormatter={(tick) => format(new Date(tick), 'MMM d')} />
                            <YAxis tick={{ fill: '#a0aec0' }} tickFormatter={(tick) => tick >= 1000 ? `${(tick/1000).toFixed(0)}k` : tick} />
                            <Tooltip
                                contentStyle={{ backgroundColor: '#2d3748', border: '1px solid #4a5568', borderRadius: '0.5rem' }}
                                labelStyle={{ color: '#e2e8f0', fontWeight: 'bold' }}
                                itemStyle={{ fontWeight: 'bold' }}
                                formatter={(value, name) => [Math.round(value).toLocaleString(), formatName(name)]}
                            />
                            <Legend wrapperStyle={{ color: '#e2e8f0' }} formatter={formatName} />
                            {selectedItems.map((key, index) => (
                                <Line 
                                  key={key} 
                                  type="monotone" 
                                  dataKey={key} 
                                  name={key}
                                  stroke={COLORS[index % COLORS.length]} 
                                  dot={chartData.length === 1} 
                                  activeDot={{ r: 8 }}
                                  strokeWidth={2} />
                            ))}
                        </LineChart>
                    </ResponsiveContainer>
                )}
            </div>
        </Card>
    );
}

// --- Main App Component ---
export default function App() {
    const [snapshotInfo, setSnapshotInfo] = useState('Loading...');
    const [isCollecting, setIsCollecting] = useState(false);

    const handleCollectData = async () => {
        setIsCollecting(true);
        setSnapshotInfo('Triggering data collection...');
        try {
            const res = await fetch(`${API_BASE_URL}/api/trigger_collect`, { method: 'POST' });
            if (res.ok) {
                setSnapshotInfo('Collection process started! Refreshing in 5s...');
                setTimeout(() => window.location.reload(), 5000); 
            } else {
                setSnapshotInfo('Failed to start collection.');
            }
        } catch (error) {
            console.error("Failed to trigger collection:", error);
            setSnapshotInfo('Error starting collection.');
        } finally {
            setTimeout(() => setIsCollecting(false), 5000);
        }
    };
    
    useEffect(() => {
        const fetchTimestamp = async () => {
            try {
                const res = await fetch(`${API_BASE_URL}/api/latest_snapshot_timestamp`);
                const data = await res.json();
                if (data.latest_timestamp) {
                    const date = new Date(data.latest_timestamp * 1000);
                    setSnapshotInfo(`Latest data: ${date.toLocaleString()}`);
                } else {
                    setSnapshotInfo('No data found. Click "Collect" to start.');
                }
            } catch (error) {
                setSnapshotInfo('Error: Could not connect to backend.');
            }
        };
        fetchTimestamp();
    }, []);

    return (
        <div className="bg-gray-900 text-gray-100 min-h-screen p-4 sm:p-8 font-sans bg-gradient-to-br from-gray-900 to-indigo-900/30">
            <header className="max-w-7xl mx-auto flex flex-col sm:flex-row justify-between items-center mb-8">
                <h1 className="text-3xl font-bold text-white">SkyBlock Stats Dashboard</h1>
                <div className="flex flex-col items-center gap-2 mt-4 sm:mt-0">
                    <button
                        onClick={handleCollectData}
                        disabled={isCollecting}
                        className="bg-indigo-600 hover:bg-indigo-700 disabled:bg-gray-500 disabled:cursor-not-allowed text-white font-bold py-2 px-4 rounded-lg transition-transform duration-200 hover:scale-105"
                    >
                        {isCollecting ? 'Collecting...' : 'Collect Latest Data'}
                    </button>
                    <p className="text-xs text-gray-400 h-4">{snapshotInfo}</p>
                </div>
            </header>

            <main className="max-w-7xl mx-auto grid grid-cols-1 lg:grid-cols-2 gap-6">
                <div className="lg:col-span-2">
                    <LatestStats />
                </div>

                <ProgressTable title="Collection Progress" apiEndpoint="collections" />
                <ProgressTable title="Bestiary Progress" apiEndpoint="bestiary" />
                
                <div className="lg:col-span-2">
                    <HistoricalChart title="Skill XP Progression" apiEndpoint="skills" />
                </div>

                <div className="lg:col-span-2">
                    <HistoricalChart title="Collection History" apiEndpoint="collections" />
                </div>

                <div className="lg:col-span-2">
                    <HistoricalChart title="Bestiary History" apiEndpoint="bestiary" />
                </div>
                
                 <div className="lg:col-span-2">
                    <HistoricalChart title="Profile Stats History" apiEndpoint="profile_stats" />
                </div>
            </main>
        </div>
    );
}