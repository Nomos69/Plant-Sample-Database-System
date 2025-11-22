
CREATE TABLE researcher (
  researcher_id SERIAL PRIMARY KEY,
  name VARCHAR(50),
  email VARCHAR(50),
  phone VARCHAR(50),
  affiliation VARCHAR(50)
);

CREATE TABLE sampling_location (
  location_id SERIAL PRIMARY KEY,
  location_attributes JSON
);

CREATE TABLE plant_sample (
  sample_id SERIAL PRIMARY KEY,
  sample_attributes JSON,
  researcher_id INTEGER REFERENCES researcher(researcher_id) ON DELETE SET NULL,
  location_id INTEGER REFERENCES sampling_location(location_id) ON DELETE SET NULL
);

CREATE TABLE environmental_condition (
  sample_id INTEGER PRIMARY KEY REFERENCES plant_sample(sample_id) ON DELETE CASCADE,
  condition_attributes JSON
);

