'use client';
import { useEffect, useRef } from 'react';

function GraphFrame({
  html,
  js_data,
  js_icons,
}: {
  html: string;
  js_data: string;
  js_icons: string;
}) {
  const iframeRef = useRef<HTMLIFrameElement>(null);

  useEffect(() => {
    if (iframeRef.current) {
      const doc =
        iframeRef.current.contentDocument ||
        iframeRef.current.contentWindow?.document;
      if (doc) {
        doc.open();
        doc.write(html);
        
        const scriptTags = doc.getElementsByTagName('script');

        for (const scripttag of scriptTags) {
          if (scripttag.src && scripttag.src.includes('data.js')) {
            scripttag.removeAttribute('src');
            scripttag.innerHTML = js_data;
            break;
          }
        }

        const script = doc.createElement('script');
        script.type = 'text/javascript';
        script.innerHTML = js_icons;
        doc.head.appendChild(script);

        doc.close();
      }
    }
  }, [html, js_data, js_icons]);

  return (
    // <div className="border rounded shadow-lg">
    <iframe
      ref={iframeRef}
      title='Dynamic HTML Content'
      className='w-full h-full'
    />
    // </div>
  );
}

export default GraphFrame;
