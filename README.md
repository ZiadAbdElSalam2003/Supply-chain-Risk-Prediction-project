<p align="center">
  <img src="images/supply.jpg" alt="Global supply chain and logistics operations" width="100%">
</p>

<h1 align="center">Late Delivery Risk Prediction</h1>

<p align="center">
  A machine learning solution for identifying at-risk shipments and supporting proactive supply-chain decisions.
</p>

## 1. Executive Overview
This project develops a supply-chain risk prediction system designed to detect orders likely to be delivered late before operational issues escalate. The objective is to support decision-makers with a proactive warning mechanism that helps prioritize at-risk shipments, reduce service disruption, and improve delivery reliability.

The project combines structured data preprocessing, exploratory analysis, feature engineering, model benchmarking, and threshold optimization to build a model aligned with real business priorities. The final system is tuned for recall, ensuring that a high proportion of actual late deliveries are identified and flagged for intervention.

## 2. Business Impact
Late deliveries have direct operational and customer-facing consequences, including:

- reduced customer trust and satisfaction
- increased fulfillment and service recovery costs
- missed SLA commitments and delivery penalties
- reduced warehouse and logistics efficiency
- weaker planning visibility across the supply chain

In practice, the cost of missing a real late-delivery case is greater than the cost of identifying a borderline case. For this reason, the model is optimized to catch as many true late-delivery events as possible, allowing teams to intervene early and reduce downstream disruption.

## 3. Model Performance
The final model selected for deployment is a tuned Random Forest classifier. After performance comparison across multiple models, the Random Forest provided the strongest balance of predictive capability and operational usefulness.

### Final Test Results
- Accuracy: 0.71
- Precision: 0.61
- Recall: 0.90
- F1-score: 0.73
- ROC-AUC: 0.78

This model is particularly effective for a risk-monitoring use case because it identifies roughly 90% of actual late-delivery cases while maintaining a practical precision level for real-world operational use.

**90% Recall — The model identifies approximately 90 out of every 100 actual late-delivery cases.**

## 4. Threshold Optimization
Decision threshold tuning was a key part of this project. The default classification threshold of 0.50 is often optimized for general accuracy, but in this business context that choice leads to too many late-delivery events being missed.

### Impact of Decision Threshold Optimization

| Threshold | Precision | Recall | F1-score |
|-----------|-----------|--------|----------|
| 0.50      | 0.82      | 0.60   | 0.69     |
| 0.33      | 0.61      | 0.90   | 0.73     |

### Key insight
Default threshold · 0.50

# **60%**
Recall

Optimized threshold · 0.33

# **90%**
Recall

# **+30 percentage points**
Improvement in late-delivery detection.

This comparison highlights the central business decision: a lower threshold increases recall substantially, which is essential when the primary objective is to catch at-risk shipments before they become late. The tuned threshold improves late-delivery detection by 30 percentage points, which is a meaningful operational gain for logistics teams.

## 5. Feature Engineering
The modeling pipeline includes a range of preprocessing steps designed to improve model robustness and predictive value:

- removal of leakage-prone and non-actionable columns
- handling of missing values and inconsistent entries
- conversion of temporal fields into structured date-based features
- encoding of categorical variables for machine learning compatibility
- numeric scaling for better model stability

The final feature set contains both behavioral and operational dimensions relevant to delivery outcome risk, providing the model with a realistic representation of the order and logistics context.

## 6. Application Architecture
The project follows a practical ML application architecture built for reuse and deployment:

- Data ingestion and preprocessing in Python
- Exploratory analysis and model experimentation in Jupyter Notebook
- Automated pipeline training using scikit-learn
- Model comparison and threshold selection for operational optimization
- Pipeline export with joblib for reproducibility
- Streamlit-based interface for interactive prediction use

The architecture supports both analytical exploration and practical application, making it suitable for internal operations dashboards or decision-support systems.

## 7. Installation & Deployment
### Local Setup
1. Clone the repository.
2. Create a Python virtual environment.
3. Install dependencies using the project requirements.
4. Run the notebook for experimentation or launch the app for predictions.

### Live Application
A live version of the application can be hosted here:

- Live Demo: [Add your link here]

This placeholder is included for easy integration of the deployed app URL once available.

## 8. Limitations & Future Improvements
While the current model delivers strong recall and operational value, there are still opportunities for improvement:

- expanding the feature set with real-time logistics and carrier data
- incorporating more granular shipment and inventory signals
- testing additional classifiers and ensemble strategies
- improving calibration for probability-based operational thresholds
- validating model performance across different regions and time periods

A future version may also include automated retraining workflows and a more advanced monitoring layer to detect model drift over time.

## Technology Stack
- Python
- pandas
- NumPy
- scikit-learn
- Matplotlib / Seaborn
- Streamlit
- joblib
- Jupyter Notebook

## Repository Structure
- `Nextgen_project_modeled.ipynb` — exploratory analysis and model training notebook
- `app_updated.py` — interactive application used for predictions
- `models/` — trained model pipeline and threshold artifacts
- `README.md` — project summary and deployment documentation

## Conclusion
This project demonstrates a practical and business-aligned machine learning solution for late-delivery risk detection. By prioritizing recall and tuning the decision threshold, the model significantly improves the ability to identify real late-delivery cases before they escalate. The result is a system that is more useful for operational teams than a model optimized only for generic accuracy metrics.
