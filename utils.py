import math
from scipy import stats
import numpy as np

def calculate_sample_size(
    effect_size,
    alpha=0.05,
    power=0.80,
    allocation_ratio=1.0,
    study_type="parallel"
):
    """
    Calculate sample size for medical research studies.
    
    Parameters:
    effect_size (float): Expected difference between groups (standardized)
    alpha (float): Significance level (Type I error rate)
    power (float): Statistical power (1 - Type II error rate)
    allocation_ratio (float): Ratio of control to treatment group sizes (n2/n1)
    study_type (str): Either "parallel" for two independent groups or "paired" for paired samples
    
    Returns:
    tuple: (n1, n2) where n1 is treatment group size and n2 is control group size
    """
    
    z_alpha = stats.norm.ppf(1 - alpha/2)
    z_beta = stats.norm.ppf(power)
    
    if study_type == "parallel":
        n1 = math.ceil(
            (2 * (z_alpha + z_beta)**2) / (effect_size**2) * 
            (1 + 1/allocation_ratio) / allocation_ratio
        )
        n2 = math.ceil(n1 * allocation_ratio)
    else:  # paired
        n1 = n2 = math.ceil(
            2 * (z_alpha + z_beta)**2 / (effect_size**2)
        )
    
    return n1, n2

def calculate_effect_size(mean1, mean2, pooled_sd):
    """
    Calculate standardized effect size (Cohen's d)
    
    Parameters:
    mean1 (float): Mean of first group
    mean2 (float): Mean of second group
    pooled_sd (float): Pooled standard deviation
    
    Returns:
    float: Standardized effect size (Cohen's d)
    """
    return abs(mean1 - mean2) / pooled_sd

def create_power_curve(effect_size, alpha, allocation_ratio, study_type):
    """
    Generate data for power curve
    
    Parameters:
    effect_size (float): Expected difference between groups (standardized)
    alpha (float): Significance level
    allocation_ratio (float): Ratio of control to treatment group sizes
    study_type (str): Study design type
    
    Returns:
    tuple: (powers, sample_sizes) arrays for plotting
    """
    powers = np.linspace(0.5, 0.99, 50)
    sample_sizes = []
    for p in powers:
        n1, _ = calculate_sample_size(effect_size, alpha, p, allocation_ratio, study_type)
        sample_sizes.append(n1)
    return powers, sample_sizes
