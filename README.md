# blumensync

Fake/dev-only sync endpoint. Simulates a streaming `/sync` endpoint: emits
progress in 10% steps at random 1-10s intervals, succeeds ~80% of runs,
fails ~20% with an error line partway through. Not connected to any real
CDN or image pipeline.
