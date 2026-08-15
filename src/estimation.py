import numpy as np
from scipy.stats import norm
import pandas as pd

def generate_data(n = 1000, seed = 42):
        rng = np.random.default_rng(seed)
        avg_age_group = rng.choice([10, 20, 30, 40, 50], size = (n, 1))
        exercise_mean = 10
        exercise_sd = 15
        cholesterol_mean = 130
        cholesterol_sd = 15
        effect_age_on_exercise = 4
        effect_age_on_cholesterol = 4
        exercise = rng.normal(exercise_mean, exercise_sd, size = (n, 1)) + effect_age_on_exercise * avg_age_group
        cholesterol = rng.normal(cholesterol_mean, cholesterol_sd, size = (n, 1)) + (-0.5) * exercise + avg_age_group * effect_age_on_cholesterol
        data = pd.DataFrame({"exercise": exercise.reshape(n), "cholesterol": cholesterol.reshape(n), "age_groups": avg_age_group.reshape(n).astype(str)})
        return data

def bivariate_regression(data, outcome_label, explanatory_label):
        n = data.shape[0]
        outcome = data[outcome_label].to_numpy().reshape((n, 1))
        explanatory = data[explanatory_label].to_numpy().reshape((n, 1))
        mean_outcome = outcome.mean()
        mean_explanatory = explanatory.mean()
        outcome_deviations = outcome - mean_outcome
        explanatory_deviations = explanatory - mean_explanatory
        beta_2 = (outcome_deviations * explanatory_deviations).sum() / (explanatory_deviations ** 2).sum()
        beta_1 = mean_outcome - mean_explanatory * beta_2
        error_deviations = outcome_deviations - explanatory_deviations * beta_2
        estimated_variance = (error_deviations ** 2).sum() / (n - 2)
        beta_2_variance = estimated_variance / (explanatory_deviations ** 2).sum()
        return beta_1, beta_2, beta_2_variance

def calculate_pvalue(beta, beta_variance):
        t_statistic = beta / np.sqrt(beta_variance)
        p_value = 2 * norm.cdf(-np.abs(t_statistic))
        return p_value

def calculate_r_squared(data, outcome_label, explanatory_label, beta_1, beta_2):
        outcome = data[outcome_label].to_numpy()
        explanatory = data[explanatory_label].to_numpy()
        fitted = beta_1 + beta_2 * explanatory
        ss_res = ((outcome - fitted) ** 2).sum()
        ss_tot = ((outcome - outcome.mean()) ** 2).sum()
        return 1 - ss_res / ss_tot

def regression_results(data, outcome_label, explanatory_label):
        n = data.shape[0]
        beta_1, beta_2, beta_2_variance = bivariate_regression(data, outcome_label, explanatory_label)
        p_value = calculate_pvalue(beta_2, beta_2_variance)
        r_squared = calculate_r_squared(data, outcome_label, explanatory_label, beta_1, beta_2)
        explanatory = data[explanatory_label].to_numpy()
        outcome = data[outcome_label].to_numpy()
        fitted = beta_1 + beta_2 * explanatory
        residuals = outcome - fitted
        mse = (residuals ** 2).sum() / (n - 2)
        mean_x = explanatory.mean()
        ss_x = ((explanatory - mean_x) ** 2).sum()
        se_fit = np.sqrt(mse * (1/n + (explanatory - mean_x)**2 / ss_x))
        results = {
                "beta_1": beta_1,
                "beta_2": beta_2,
                "p_value": p_value,
                "r_squared": r_squared,
                "mse": mse,
                "mean_x": mean_x,
                "ss_x": ss_x,
                "n": n
        }
        return results

def disaggregated_fits(data, explanatory_label, group_variable, results):
        data["disaggregated_beta1"] = data[group_variable].apply(lambda row: results[row]["beta_1"])
        data["disaggregated_beta2"] = data[group_variable].apply(lambda row: results[row]["beta_2"])
        disaggregated_fit = data["disaggregated_beta1"] + data["disaggregated_beta2"] * data[explanatory_label]
        return disaggregated_fit


def execute_regressions(data: pd.DataFrame, outcome_label = "cholesterol", explanatory_label = "exercise", group_variable = "age_groups"):
        results = {
                "segregated": {}, 
                "aggregated": regression_results(data, outcome_label, explanatory_label)
        }
        for age, group in data.groupby(group_variable):
                results["segregated"].update({age: regression_results(group, outcome_label, explanatory_label)})
        aggregated = results["aggregated"]
        data["aggregated_fit"] = aggregated["beta_1"] + aggregated["beta_2"] * data[explanatory_label]
        x = data[explanatory_label].to_numpy()
        se_agg = np.sqrt(aggregated["mse"] * (1/aggregated["n"] + (x - aggregated["mean_x"])**2 / aggregated["ss_x"]))
        data["aggregated_ci_upper"] = data["aggregated_fit"] + 1.96 * se_agg
        data["aggregated_ci_lower"] = data["aggregated_fit"] - 1.96 * se_agg
        data["disaggregated_fit"] = disaggregated_fits(data, explanatory_label, group_variable, results["segregated"])
        for age, group_results in results["segregated"].items():
                mask = data[group_variable] == age
                x_group = data.loc[mask, explanatory_label].to_numpy()
                se_group = np.sqrt(group_results["mse"] * (1/group_results["n"] + (x_group - group_results["mean_x"])**2 / group_results["ss_x"]))
                data.loc[mask, "disaggregated_ci_upper"] = data.loc[mask, "disaggregated_fit"].to_numpy() + 1.96 * se_group
                data.loc[mask, "disaggregated_ci_lower"] = data.loc[mask, "disaggregated_fit"].to_numpy() - 1.96 * se_group
        return results, data



