-- Rheology experiment database schema (SQLite)

PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS experiments (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    sample_name          TEXT    NOT NULL,
    geometry             TEXT    NOT NULL,   -- 'cone_plate' | 'cup_bob' | 'vane_cup'
    gap_m               REAL,               -- cone/plate: gap (m). For other geometries can be NULL.
    r1_m                REAL,               -- inner radius (m) for bob/vane
    r2_m                REAL,               -- cup radius (m) for cup/bob or vane/cup
    yield_stress0_Pa    REAL,               -- initial guess for yield stress (Pa) for HB fit
    notes               TEXT,
    created_at          TEXT    NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS measurements (
    id                      INTEGER PRIMARY KEY AUTOINCREMENT,
    experiment_id            INTEGER NOT NULL,
    row_index                INTEGER NOT NULL,
    segment                  TEXT, -- 'up' | 'down' | NULL
    shear_rate_1_s           REAL,
    shear_stress_Pa          REAL,
    viscosity_Pa_s           REAL,
    target_shear_rate_1_s    REAL,
    percentage_deviation_pct REAL,
    temperature_C            REAL,
    time_s                   REAL,
    thrust_g                 REAL,
    accumulated_time_s       REAL,
    torque_Nm                REAL,
    angular_velocity_rad_s   REAL,
    notes                    TEXT,
    FOREIGN KEY (experiment_id) REFERENCES experiments(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_measurements_experiment ON measurements(experiment_id);
CREATE INDEX IF NOT EXISTS idx_measurements_experiment_segment ON measurements(experiment_id, segment);

CREATE TABLE IF NOT EXISTS fit_results (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    experiment_id        INTEGER NOT NULL,
    segment              TEXT    NOT NULL, -- 'all' | 'up' | 'down'
    model                TEXT    NOT NULL, -- 'power_law' | 'bingham' | 'herschel_bulkley'
    tau_y_Pa             REAL,             -- HB: tau_y
    K                    REAL,             -- power law/HB
    n                    REAL,             -- power law/HB
    tau0_Pa              REAL,             -- Bingham: intercept
    mu_Pa_s              REAL,             -- Bingham: slope
    r_squared            REAL,
    n_points             INTEGER,
    method               TEXT,
    created_at           TEXT    NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (experiment_id) REFERENCES experiments(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_fit_results_experiment ON fit_results(experiment_id);

CREATE TABLE IF NOT EXISTS derived_metrics (
    experiment_id            INTEGER PRIMARY KEY,
    hysteresis_area_Pa_s     REAL,   -- area between up/down curves in tau(gamma_dot): ∫ |τ_up-τ_down| dγ̇
    hysteresis_area_method   TEXT,
    tau1c_up_Pa              REAL,   -- τ1,c = τy*(r2/r1)^2 computed from HB fit (up)
    tau1c_down_Pa            REAL,   -- same for down
    tau1c_all_Pa             REAL,   -- same for all (if no up/down)
    tauy_up_Pa               REAL,
    tauy_down_Pa             REAL,
    tauy_all_Pa              REAL,
    created_at               TEXT    NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (experiment_id) REFERENCES experiments(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS artifacts (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    experiment_id    INTEGER NOT NULL,
    kind            TEXT NOT NULL,   -- 'fig1'|'fig2'|'fig3'|'fig4'|'summary_csv'|'report_pdf'
    path            TEXT NOT NULL,
    created_at      TEXT NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (experiment_id) REFERENCES experiments(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_artifacts_experiment ON artifacts(experiment_id);
