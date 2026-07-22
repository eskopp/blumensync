# flora-incognita (factsheet_images fake sync)

Fake/dev-only stand-in for the production `factsheet_images` service used by
flora-stories-editor (`FACTSHEET_IMAGES_SYNC_URL`). Simulates the real
streaming `/sync` endpoint: emits progress in 10% steps at random 1-10s
intervals, succeeds ~80% of runs, fails ~20% with an error line partway
through. Not connected to any real CDN or image pipeline.
