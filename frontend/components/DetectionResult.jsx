/**
 * Detection result display component
 */
export default function DetectionResult({ prediction, error, drowsyStreak = 0, isAlarming = false }) {
  if (error) {
    return (
      <div className="card bg-red-50 dark:bg-red-900/20 border-2 border-red-500">
        <div className="flex items-start space-x-3">
          <svg className="w-6 h-6 text-red-500 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <div>
            <h3 className="text-lg font-semibold text-red-700 dark:text-red-300">Error</h3>
            <p className="text-sm text-red-600 dark:text-red-400 mt-1">{error}</p>
          </div>
        </div>
      </div>
    );
  }

  if (!prediction) {
    return (
      <div className="card border-2 border-dashed border-gray-300 dark:border-gray-600">
        <div className="text-center text-gray-500 dark:text-gray-400 py-8">
          <svg className="w-16 h-16 mx-auto mb-4 text-gray-400 dark:text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z" />
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M15 13a3 3 0 11-6 0 3 3 0 016 0z" />
          </svg>
          <p className="text-lg font-medium">No detection yet</p>
          <p className="text-sm mt-1">Start live monitoring or capture a frame</p>
        </div>
      </div>
    );
  }

  const { label, confidence, status, all_probs } = prediction;
  const isDrowsy = status === 'drowsy';

  return (
    <div className="space-y-4">
      {/* Alarm banner */}
      {isAlarming && (
        <div className="flex items-center gap-3 px-4 py-3 bg-red-600 text-white rounded-xl font-bold text-lg animate-pulse shadow-lg">
          <span className="text-2xl">🚨</span>
          <span>DROWSINESS ALERT! Please rest.</span>
        </div>
      )}

      {/* Main result card */}
      <div className={`card ${isDrowsy
        ? 'bg-red-50 dark:bg-red-900/20 border-2 border-red-500'
        : 'bg-green-50 dark:bg-green-900/20 border-2 border-green-500'}`}
      >
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-4">
            {/* Status icon */}
            <div className={`w-16 h-16 rounded-full flex items-center justify-center flex-shrink-0 ${isDrowsy ? 'bg-red-500' : 'bg-green-500'}`}>
              {isDrowsy ? (
                <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                </svg>
              ) : (
                <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              )}
            </div>

            {/* Status text */}
            <div>
              <h2 className={`text-2xl font-bold ${isDrowsy ? 'text-red-700 dark:text-red-300' : 'text-green-700 dark:text-green-300'}`}>
                {isDrowsy ? '😴 Drowsy Detected' : '✅ Driver Alert'}
              </h2>
              <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">
                Class: <span className="font-semibold">{label}</span>
              </p>
              {isDrowsy && drowsyStreak > 0 && (
                <p className="text-xs text-red-600 dark:text-red-400 mt-1 font-medium">
                  🔁 {drowsyStreak} consecutive drowsy frame{drowsyStreak > 1 ? 's' : ''}
                </p>
              )}
            </div>
          </div>

          {/* Confidence */}
          <div className="text-right flex-shrink-0">
            <div className={`text-3xl font-bold ${isDrowsy ? 'text-red-700 dark:text-red-300' : 'text-green-700 dark:text-green-300'}`}>
              {(confidence * 100).toFixed(1)}%
            </div>
            <div className="text-xs text-gray-500 dark:text-gray-400">Confidence</div>
          </div>
        </div>

        {/* Confidence bar */}
        <div className="mt-4">
          <div className="flex justify-between text-xs mb-1 text-gray-500 dark:text-gray-400">
            <span>Confidence Level</span>
            <span>{(confidence * 100).toFixed(2)}%</span>
          </div>
          <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-3 overflow-hidden">
            <div
              className={`h-full rounded-full transition-all duration-300 ${isDrowsy ? 'bg-red-500' : 'bg-green-500'}`}
              style={{ width: `${confidence * 100}%` }}
            />
          </div>
        </div>
      </div>

      {/* Class probabilities */}
      {all_probs && Object.keys(all_probs).length > 0 && (
        <div className="card">
          <h3 className="text-sm font-semibold text-gray-700 dark:text-gray-300 mb-3">
            Class Probabilities
          </h3>
          <div className="space-y-2">
            {Object.entries(all_probs)
              .sort((a, b) => b[1] - a[1])
              .slice(0, 5)
              .map(([className, prob]) => (
                <div key={className}>
                  <div className="flex justify-between text-xs mb-1">
                    <span className="font-medium text-gray-600 dark:text-gray-400 capitalize">
                      {className.replace(/_/g, ' ')}
                    </span>
                    <span className="text-gray-500 dark:text-gray-500">
                      {(prob * 100).toFixed(1)}%
                    </span>
                  </div>
                  <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                    <div
                      className="bg-blue-500 h-full rounded-full transition-all duration-300"
                      style={{ width: `${prob * 100}%` }}
                    />
                  </div>
                </div>
              ))}
          </div>
        </div>
      )}
    </div>
  );
}
