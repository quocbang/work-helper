import re

pattern = r"https.*?/ "  # Use non-greedy matching to avoid over-capturing

match = re.search(
    pattern,
    "0.53 fbN:/ 07/25 v@s.RX 《高处营救》全集，2024年最新末日大片震撼来袭！非常精彩 # 一口气看完系列 # 影视解说 # 每日推荐电影 # 惊险刺激  https://v.douyin.com/dDaA2ScRcgY/ 复制此链接，打开Dou音搜索，直接观看视频！",
)
if match:
    print(match.group(0))  # Output the matched URL
