import React from 'react';

interface ColorSwatchProps {
  color: string;
  name: string;
  className?: string;
}

const ColorSwatch = ({ color, name, className = '' }: ColorSwatchProps) => (
  <div className="flex flex-col items-center">
    <div 
      className={`w-16 h-16 rounded-md shadow-md ${className}`} 
      style={{ backgroundColor: color }}
    ></div>
    <span className="mt-2 text-sm font-medium">{name}</span>
    <span className="text-xs text-muted-foreground">{color}</span>
  </div>
);

export function ThemeGuide() {
  return (
    <div className="p-6 space-y-8 max-w-4xl mx-auto">
      <div>
        <h2 className="text-2xl font-semibold mb-4">Brand Colors</h2>
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-6">
          <ColorSwatch color="#77eaa2" name="Primary" className="border" />
          <ColorSwatch color="#7de03f" name="Secondary" className="border" />
          <ColorSwatch color="#e03f88" name="Accent" className="border" />
          <ColorSwatch color="#614c55" name="Gray Purple" className="border" />
          <ColorSwatch color="#4c6153" name="Gray Green" className="border" />
          <ColorSwatch color="#54614C" name="Olive Green" className="border" />
        </div>
      </div>

      <div>
        <h2 className="text-2xl font-semibold mb-4">UI Components</h2>
        <div className="grid gap-4">
          <div className="flex flex-col gap-2">
            <button className="bg-primary text-primary-foreground px-4 py-2 rounded-md">
              Primary Button
            </button>
            <button className="bg-secondary text-secondary-foreground px-4 py-2 rounded-md">
              Secondary Button
            </button>
            <button className="bg-accent text-accent-foreground px-4 py-2 rounded-md">
              Accent Button
            </button>
            <button className="bg-muted text-muted-foreground px-4 py-2 rounded-md">
              Muted Button
            </button>
            <button className="bg-destructive text-destructive-foreground px-4 py-2 rounded-md">
              Destructive Button
            </button>
          </div>

          <div className="p-4 bg-card text-card-foreground border rounded-md shadow-sm">
            <h3 className="text-lg font-medium">Card Example</h3>
            <p className="text-muted-foreground">This is a card with the new styling.</p>
          </div>

          <div className="flex gap-2">
            <div className="p-3 bg-success text-success-foreground rounded-md">Success</div>
            <div className="p-3 bg-warning text-warning-foreground rounded-md">Warning</div>
            <div className="p-3 bg-destructive text-destructive-foreground rounded-md">Error</div>
          </div>
        </div>
      </div>

      <div>
        <h2 className="text-2xl font-semibold mb-4">Minimalist Design Examples</h2>
        <div className="grid md:grid-cols-2 gap-6">
          <div className="p-4 bg-white border rounded-lg shadow-sm">
            <div className="h-32 bg-brandGreen/10 rounded-md flex items-center justify-center">
              <div className="w-16 h-16 bg-brandGreen rounded-full"></div>
            </div>
            <h3 className="mt-4 text-lg font-medium">Clean Card</h3>
            <p className="text-muted-foreground">Simple, clean design with subtle color accents.</p>
          </div>
          
          <div className="p-4 bg-white border rounded-lg shadow-sm">
            <div className="h-32 bg-brandPink/10 rounded-md flex items-center justify-center">
              <div className="h-8 w-32 bg-brandPink rounded-md"></div>
            </div>
            <h3 className="mt-4 text-lg font-medium">Minimal UI</h3>
            <p className="text-muted-foreground">Focused on content with just enough color.</p>
          </div>
        </div>
      </div>
    </div>
  );
} 