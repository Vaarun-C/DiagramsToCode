export default function FileDisplay({ files }) {
    if (files.length === 0) {
      return <p className="text-gray-500 text-center">No files uploaded yet</p>;
    }
  
    return (
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {files.map((file, index) => (
          <div key={index} className="border rounded-lg p-4 shadow-sm">
            {file.type.startsWith('image/') ? (
              <img 
                src={file.url} 
                alt={file.name}
                className="w-full h-48 object-cover rounded-lg mb-2"
              />
            ) : (
              <div className="w-full h-48 bg-gray-100 rounded-lg mb-2 flex items-center justify-center">
                <p className="text-gray-500">{file.type}</p>
              </div>
            )}
            <p className="font-medium truncate">{file.name}</p>
            <p className="text-sm text-gray-500">
              {(file.size / 1024).toFixed(2)} KB
            </p>
          </div>
        ))}
      </div>
    );
  }