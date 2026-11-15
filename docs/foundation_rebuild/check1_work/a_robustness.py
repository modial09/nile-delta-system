"""Check 1, script A: recompute the robustness statistics from the saved
sample file. Independent of the model code; reads only the CSV."""
import pandas as pd

df = pd.read_csv("/home/hatch/workspace/mit-projects/nile-delta-system/"
                 "data/processed/robustness_samples_v4_1.csv")
print("rows:", len(df), "columns:", list(df.columns))
s = df["share_percent"]
sf = df["shortfall_tonnes"]
print(f"min share      {s.min():.4f}")
print(f"p10 share (pandas linear) {s.quantile(0.10):.4f}")
print(f"p10 share (nearest rank)  {s.sort_values().iloc[int(0.10*len(s))]:.4f}")
print(f"median share   {s.median():.4f}")
print(f"mean share     {s.mean():.4f}")
print(f"max share      {s.max():.4f}")
print(f"max staple t   {df['max_staple_tonnes'].max():,.1f}")
holds = (s >= 80.0).mean() * 100
print(f"share of samples at or above 80 percent: {holds:.1f}")
worst = sf.sort_values(ascending=False).head(len(sf) // 10)
print(f"worst decile n={len(worst)} mean shortfall {worst.mean():,.1f}")
print(f"mean shortfall all samples {sf.mean():,.1f}")
print("kinds:", df["kind"].value_counts().to_dict())
print("budget range:", df["budget_billion_cubic_metres"].min(),
      df["budget_billion_cubic_metres"].max())
# consistency: shortfall should equal max(0, 9803525.6 - max_staple)
ref = 12254407.0
target = 0.80 * ref
chk = (df["shortfall_tonnes"] - (target - df["max_staple_tonnes"]).clip(lower=0)).abs()
print("max shortfall identity error:", chk.max())
chk2 = (df["share_percent"] - 100 * df["max_staple_tonnes"] / ref).abs()
print("max share identity error:", chk2.max())
