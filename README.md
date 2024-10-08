Here’s a sample `README.md` for your project:

```markdown
# Production Planner V0.1

Production Planner is a Python-based tool designed to assist with scheduling and forecasting production across multiple production lines. The tool supports two main functionalities:
1. Calculate units produced given a number of hours worked.
2. Calculate hours required to meet a given production target.

## Features

- Calculate production based on input data for Wetpacks and Vases.
- Generate production schedules for up to four production lines.
- Create detailed visualizations including demand and production curves, daily production, and line-specific breakdowns.
- Export results to CSV files for further analysis.
- Generate PDF reports summarizing the production projections and schedules.

## Requirements

To run this project, the following Python libraries are required:
- `pandas`
- `numpy`
- `matplotlib`

You can install them using `pip`:
```bash
pip install pandas numpy matplotlib
```

## Project Structure

- **input/**: Contains CSV files with input data. Example files are:
  - `HOURS.csv` (when calculating units from hours)
  - `UNITS.csv` (when calculating hours from units)
- **output/**: This folder will contain generated production schedules, overview data, and PDF reports.

## How to Use

1. **Run the program**:
   ```
   python production_planner.py
   ```
   You will be prompted to select a mode:
   - Option 1: Calculate units given hours worked.
   - Option 2: Calculate hours required for a specific production target.

2. **Input data**: The program expects CSV files with demand data and production hours or production units. Ensure that your data is formatted correctly before running the program.

3. **Output**: The program generates:
   - `prod_schedule.csv` – a detailed schedule of hours or units per production line.
   - `overview_data.csv` – an overview of the production and demand data.
   - PDF report with visual summaries of production and demand trends.

## Visualizations

The program generates several visual reports including:
- Wetpacks and vases demand curves.
- Daily production and storage pallets.
- Per-line production views.
- A detailed schedule projection.

These visualizations are exported as a PDF file, located in the `output/` folder, with the name format: `Projection[start_date-end_date].pdf`.

## Example Input Format

Sample format for `HOURS.csv` or `UNITS.csv` (columns):

| Dia        | WP Demand | Vases Demand | LINE1_WP_HOURS | LINE1_VASE_HOURS | ... |
|------------|------------|--------------|----------------|------------------|-----|
| 01,01,2024 | 100        | 50           | 8              | 6                | ... |

## Future Enhancements

- Adding support for different product types beyond Wetpacks and Vases.
- Enhancing the scheduling algorithm to account for overtime and variable shift lengths.
- Integration with ERP systems for real-time data input.

## Contributing

Feel free to fork the repository, submit pull requests, and open issues if you encounter any bugs or have ideas for improvements.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more information.
```

This `README.md` provides an overview of the project, instructions for setup and usage, and information on future development and contributions. Adjust any project-specific details as needed.
