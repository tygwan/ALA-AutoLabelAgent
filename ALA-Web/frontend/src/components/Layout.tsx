import React from 'react';
import { Layout as LayoutIcon, Image as ImageIcon, Settings as SettingsIcon } from 'lucide-react';
import clsx from 'clsx';

interface LayoutProps {
    children: React.ReactNode;
    activePage: string;
    onNavigate: (page: string) => void;
}

export const Layout: React.FC<LayoutProps> = ({ children, activePage, onNavigate }) => {
    const navItems = [
        { id: 'annotate', label: 'Annotate', icon: ImageIcon },
        { id: 'preprocessing', label: 'Preprocessing', icon: LayoutIcon },
        { id: 'gallery', label: 'Gallery', icon: LayoutIcon },
        { id: 'settings', label: 'Settings', icon: SettingsIcon },
    ];

    return (
        <div className="flex h-screen bg-gray-900 text-white">
            {/* Sidebar */}
            <aside className="w-64 bg-gray-800 border-r border-gray-700 flex flex-col">
                <div className="p-4 border-b border-gray-700">
                    <h1 className="text-xl font-bold bg-gradient-to-r from-blue-400 to-purple-500 bg-clip-text text-transparent">
                        ALA-Web
                    </h1>
                </div>

                <nav className="flex-1 p-4 space-y-2">
                    {navItems.map((item) => (
                        <button
                            key={item.id}
                            onClick={() => onNavigate(item.id)}
                            className={clsx(
                                "flex items-center gap-3 px-3 py-2 rounded-lg w-full text-left transition-colors",
                                activePage === item.id
                                    ? "bg-blue-600 text-white"
                                    : "text-gray-400 hover:bg-gray-700 hover:text-white"
                            )}
                        >
                            <item.icon size={20} />
                            <span>{item.label}</span>
                        </button>
                    ))}
                </nav>

                <div className="p-4 border-t border-gray-700">
                    <div className="text-xs text-gray-500">v0.1.0 Alpha</div>
                </div>
            </aside>

            {/* Main Content */}
            <main className="flex-1 overflow-hidden relative">
                {children}
            </main>
        </div>
    );
};
