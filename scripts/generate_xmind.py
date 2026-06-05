from __future__ import annotations

import hashlib
import json
import time
import uuid
import zipfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable
from xml.etree import ElementTree as ET
from xml.sax.saxutils import escape


ROOT = Path(__file__).resolve().parents[1]
PRIMARY_XMIND = ROOT / "AI使用速查课_思维导图.xmind"
XMIND8_XMIND = ROOT / "AI使用速查课_思维导图_XMind8.xmind"
JSON_FALLBACK_XMIND = ROOT / "AI使用速查课_思维导图_新版JSON备选.xmind"

PNG_1X1 = bytes.fromhex(
    "89504e470d0a1a0a0000000d49484452000000010000000108060000001f15c489"
    "0000000a49444154789c6360000002000100ff0ff3d40000000049454e44ae426082"
)


@dataclass
class Topic:
    title: str
    children: list["Topic"] = field(default_factory=list)


def t(title: str, children: Iterable[Topic] = ()) -> Topic:
    return Topic(title=title, children=list(children))


MINDMAP = t(
    "AI 使用速查课",
    [
        t(
            "AI 总地图",
            [
                t(
                    "AI（人工智能）：感知、学习、推理、决策",
                    [
                        t(
                            "传统AI：规则明确、边界清楚",
                            [
                                t("规则系统：靠人工写规则"),
                                t("搜索规划：在有限状态里找路径"),
                            ],
                        ),
                        t("机器学习：从数据中归纳规律", [t("效果取决于数据和特征")]),
                        t(
                            "深度学习：神经网络自动学习表征",
                            [
                                t("视觉AI：识别、检测、理解图像"),
                                t("语言AI：理解和生成文本"),
                                t("强化学习：通过奖励学习行动策略"),
                                t("生成式AI：生成文本、代码、图像、音频、视频"),
                            ],
                        ),
                    ],
                )
            ],
        ),
        t(
            "LLM 本体",
            [
                t(
                    "LLM（当前主流）",
                    [
                        t("概念定位：生成式 AI 的核心代表；不是 AI 的全部；当前阶段最重要、最受关注"),
                        t(
                            "代表产品 / 应用",
                            [t("ChatGPT"), t("Claude"), t("Gemini"), t("DeepSeek")],
                        ),
                        t(
                            "如何认知 AI 的作用",
                            [
                                t("放大：效率倍增 -> 价值"),
                                t("补充：新能力 -> 回流到放大"),
                                t("基础能力决定放大倍数"),
                                t("技能广度决定场景数"),
                            ],
                        ),
                    ],
                )
            ],
        ),
        t(
            "大模型差异化",
            [
                t(
                    "分化来源：能力、成本、部署边界可能完全不同",
                    [
                        t(
                            "场景定位",
                            [
                                t("通用模型：覆盖广，适合邮件、总结、翻译、学习"),
                                t("垂直模型：场景窄，但术语、流程和行业任务更准"),
                            ],
                        ),
                        t(
                            "开放与控制",
                            [
                                t("闭源服务：网页/App/API 使用，厂商维护，省心但受限"),
                                t("开源/开放权重：可下载、可本地化、可定制，但要技术和运维"),
                                t("自部署关注：许可、显存、上下文、并发、KV cache、硬件采购"),
                            ],
                        ),
                        t(
                            "区域生态",
                            [
                                t("国内模型：中文、本土知识、合规、访问稳定"),
                                t("国外模型：英文、前沿能力、复杂代码仍常有优势"),
                            ],
                        ),
                        t(
                            "规模与架构",
                            [
                                t("参数规模：大参数上限高但慢贵；小参数快便宜"),
                                t("MoE：总参数大、激活参数少，兼顾能力和成本"),
                            ],
                        ),
                        t(
                            "输入输出形态",
                            [
                                t("语言大模型：文本最成熟，是办公场景核心"),
                                t("多模态：图文理解、文档分析、视觉问答"),
                                t("图像/音频/视频：专攻单一模态内容生产"),
                                t("Embedding：输出向量，不生成自然语言"),
                                t("Agent / 工具调用：以语言模型为内核，做多步工具协作"),
                            ],
                        ),
                        t(
                            "使用入口",
                            [
                                t("网页/App 订阅：适合个人和日常直接使用"),
                                t("API：适合开发集成、自动化和企业系统"),
                                t("本地部署：适合隐私敏感、离线、研究和私有化"),
                            ],
                        ),
                    ],
                )
            ],
        ),
        t(
            "能力价格与选型",
            [
                t(
                    "比较口径：不要只看排行榜，把能力、价格、边界放到同一张表",
                    [
                        t("能力维度", [t("推理 / 代码 / 中文"), t("长上下文 / 多模态 / Agent 稳定性")]),
                        t(
                            "API 成本维度",
                            [
                                t("价格字段：输入 / 输出 / 缓存 / 思考"),
                                t("单次费用：输入 + 可见输出 + 思考 + 缓存 + 工具/重试"),
                                t("成本变量：上下文、输出长度、thinking budget、调用量、重试、折扣"),
                            ],
                        ),
                        t(
                            "梯队和图形",
                            [
                                t("国内/国外 T0、T1：只作初筛，不是永久排名"),
                                t("价格 / 性能 / 性价比柱形图：看清口径，尤其是 1:1 思考总价"),
                            ],
                        ),
                        t(
                            "部署和数据边界",
                            [
                                t("数据控制：公共云、企业通道、本地部署的风险不同"),
                                t("采购成本：开放权重不等于便宜，T0 自部署常是百万级硬件量级"),
                            ],
                        ),
                    ],
                ),
                t(
                    "选型决策：先定义任务，再选模型",
                    [
                        t(
                            "任务画像",
                            [
                                t("风险等级：合同、医疗、法律、代码架构属于高风险"),
                                t("调用频率：高频任务价格、吞吐、缓存命中更重要"),
                                t("任务类型：中文、长文档、代码、Agent、抽取、改写要分开测"),
                            ],
                        ),
                        t(
                            "决策规则",
                            [
                                t("高风险任务：先能力，再验证，再价格"),
                                t("高频低风险任务：先价格、吞吐、缓存命中"),
                                t("思考模型：必须看实际 usage 里的 reasoning/thinking token"),
                                t("长上下文任务：单独实测延迟、缓存命中和工具结果膨胀"),
                                t("最终用真实任务测试：同一批任务比较质量、速度、成本、失败率"),
                            ],
                        ),
                    ],
                ),
            ],
        ),
        t(
            "如何正确让 AI 工作",
            [
                t(
                    "让 AI 工作是控制问题：控制输入，观察输出，逐步逼近目标",
                    [
                        t("明确目标：先说要达成什么，不从工具能力出发"),
                        t("缩小空间：每条约束都在排除错误输出"),
                        t("观察反馈：看内容、格式、准确性是否达标"),
                        t("迭代逼近：每轮只修最大偏差，避免方向振荡"),
                        t("验证边界：提示词无法可靠约束事实、数字、引用和专业责任"),
                        t("分级控制：低风险轻控制；中风险反馈调节；高风险强控制"),
                    ],
                ),
                t(
                    "可控制变量和方法",
                    [
                        t("核心概念：可能性空间 / 控制 / 黑箱"),
                        t("可控制变量：提示词定方向；模型定上限；参数定稳定性/发散度"),
                        t("提示词结构：角色 / 任务 / 背景 / 格式 / 标准"),
                        t("上下文管理：重贴关键背景、分段处理、复述目标"),
                    ],
                ),
                t(
                    "验证与信任",
                    [
                        t("验证方法：官方来源、搜索核验、交叉验证、回到原文、多模型对比"),
                        t("信任分级：改写润色高；总结翻译中；数据日期引用低；医疗法律金融不信任"),
                    ],
                ),
            ],
        ),
    ],
)


def topic_id(path: str) -> str:
    return str(uuid.uuid5(uuid.NAMESPACE_URL, f"ai-ke/{path}"))


def compact_id(path: str) -> str:
    return hashlib.md5(path.encode("utf-8")).hexdigest()[:26]


def iter_topics(topic: Topic) -> Iterable[Topic]:
    yield topic
    for child in topic.children:
        yield from iter_topics(child)


def build_legacy_topic_xml(topic: Topic, path: str, timestamp: int) -> str:
    attrs = f'id="{compact_id(path)}" timestamp="{timestamp}"'
    parts = [f"<topic {attrs}><title>{escape(topic.title)}</title>"]
    if topic.children:
        parts.append('<children><topics type="attached">')
        for index, child in enumerate(topic.children, 1):
            parts.append(build_legacy_topic_xml(child, f"{path}.{index}", timestamp))
        parts.append("</topics></children>")
    parts.append("</topic>")
    return "".join(parts)


def build_legacy_content_xml(root: Topic) -> str:
    timestamp = int(time.time() * 1000)
    topic_xml = build_legacy_topic_xml(root, "root", timestamp)
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="no"?>'
        f'<xmap-content timestamp="{timestamp}" version="2.0" '
        'xmlns="urn:xmind:xmap:xmlns:content:2.0" '
        'xmlns:fo="http://www.w3.org/1999/XSL/Format" '
        'xmlns:svg="http://www.w3.org/2000/svg" '
        'xmlns:xhtml="http://www.w3.org/1999/xhtml" '
        'xmlns:xlink="http://www.w3.org/1999/xlink">'
        f'<sheet id="{compact_id("sheet")}" timestamp="{timestamp}">'
        f"{topic_xml}"
        f"<title>{escape(root.title)}</title>"
        "</sheet>"
        "</xmap-content>"
    )


def build_styles_xml() -> str:
    return (
        '<?xml version="1.0" encoding="utf-8"?>'
        '<xmap-styles version="2.0" '
        'xmlns="urn:xmind:xmap:xmlns:style:2.0" '
        'xmlns:fo="http://www.w3.org/1999/XSL/Format" '
        'xmlns:svg="http://www.w3.org/2000/svg"/>'
    )


def build_comments_xml() -> str:
    return (
        '<?xml version="1.0" encoding="utf-8"?>'
        '<comments version="2.0" xmlns="urn:xmind:xmap:xmlns:comments:2.0"/>'
    )


def topic_to_json(topic: Topic, path: str) -> dict:
    item = {
        "id": topic_id(path),
        "title": topic.title,
    }
    if path == "root":
        item["class"] = "topic"
        item["structureClass"] = "org.xmind.ui.logic.right"
    if topic.children:
        item["children"] = {
            "attached": [
                topic_to_json(child, f"{path}.{index}")
                for index, child in enumerate(topic.children, 1)
            ],
            "detached": [],
        }
    return item


def first_layer_ids(root: Topic) -> list[str]:
    return [topic_id("root")] + [
        topic_id(f"root.{index}") for index, _ in enumerate(root.children, 1)
    ]


def build_theme() -> dict:
    font = "'NeverMind','Microsoft YaHei','PingFang SC','Microsoft JhengHei','sans-serif',sans-serif"
    common_text = {
        "fo:font-family": font,
        "fo:font-style": "normal",
        "fo:color": "inherited",
        "fo:text-transform": "manual",
        "fo:text-decoration": "none",
    }
    return {
        "map": {
            "id": topic_id("theme.map"),
            "properties": {
                "svg:fill": "#FFFFFF",
                "color-list": "#2563EB #16A34A #EA580C #7C3AED #0891B2 #111827",
                "line-tapered": "none",
            },
        },
        "centralTopic": {
            "id": topic_id("theme.centralTopic"),
            "properties": {
                **common_text,
                "fo:font-size": "28pt",
                "fo:font-weight": "600",
                "fo:text-align": "center",
                "svg:fill": "#2563EB",
                "fill-pattern": "solid",
                "line-width": "2pt",
                "line-color": "#2563EB",
                "line-pattern": "solid",
                "border-line-color": "inherited",
                "border-line-width": "0pt",
                "border-line-pattern": "inherited",
                "shape-class": "org.xmind.topicShape.roundedRect",
                "line-class": "org.xmind.branchConnection.roundedfold",
                "arrow-end-class": "org.xmind.arrowShape.none",
            },
        },
        "mainTopic": {
            "id": topic_id("theme.mainTopic"),
            "properties": {
                **common_text,
                "fo:font-size": "18pt",
                "fo:font-weight": "600",
                "fo:text-align": "left",
                "svg:fill": "#111827",
                "fill-pattern": "solid",
                "line-width": "inherited",
                "line-color": "inherited",
                "line-pattern": "inherited",
                "border-line-color": "inherited",
                "border-line-width": "0pt",
                "border-line-pattern": "inherited",
                "shape-class": "org.xmind.topicShape.roundedRect",
                "line-class": "org.xmind.branchConnection.roundedElbow",
                "arrow-end-class": "inherited",
            },
        },
        "subTopic": {
            "id": topic_id("theme.subTopic"),
            "properties": {
                **common_text,
                "fo:font-size": "14pt",
                "fo:font-weight": "400",
                "fo:text-align": "left",
                "svg:fill": "#FFFFFF",
                "fill-pattern": "solid",
                "line-width": "inherited",
                "line-color": "inherited",
                "line-pattern": "inherited",
                "border-line-color": "inherited",
                "border-line-width": "0pt",
                "border-line-pattern": "inherited",
                "shape-class": "org.xmind.topicShape.roundedRect",
                "line-class": "org.xmind.branchConnection.roundedElbow",
                "arrow-end-class": "inherited",
            },
        },
        "floatingTopic": {
            "id": topic_id("theme.floatingTopic"),
            "properties": {
                **common_text,
                "fo:font-size": "14pt",
                "fo:font-weight": "400",
                "fo:text-align": "center",
                "svg:fill": "#EA580C",
                "fill-pattern": "solid",
                "line-width": "inherited",
                "line-color": "inherited",
                "line-pattern": "solid",
                "border-line-color": "#EA580C",
                "border-line-width": "0pt",
                "border-line-pattern": "inherited",
                "shape-class": "org.xmind.topicShape.roundedRect",
                "line-class": "org.xmind.branchConnection.roundedElbow",
                "arrow-end-class": "org.xmind.arrowShape.none",
            },
        },
        "summaryTopic": {
            "id": topic_id("theme.summaryTopic"),
            "properties": {
                **common_text,
                "fo:font-size": "14pt",
                "fo:font-weight": "400",
                "fo:text-align": "center",
                "svg:fill": "#111827",
                "fill-pattern": "none",
                "line-width": "inherited",
                "line-color": "inherited",
                "line-pattern": "inherited",
                "border-line-color": "#111827",
                "border-line-width": "inherited",
                "border-line-pattern": "inherited",
                "shape-class": "org.xmind.topicShape.roundedRect",
                "line-class": "org.xmind.branchConnection.roundedElbow",
                "arrow-end-class": "inherited",
            },
        },
        "calloutTopic": {
            "id": topic_id("theme.calloutTopic"),
            "properties": {
                **common_text,
                "fo:font-size": "14pt",
                "fo:font-weight": "600",
                "fo:text-align": "left",
                "svg:fill": "#111827",
                "fill-pattern": "solid",
                "line-width": "inherited",
                "line-color": "inherited",
                "line-pattern": "inherited",
                "border-line-color": "#111827",
                "border-line-width": "inherited",
                "border-line-pattern": "inherited",
                "shape-class": "org.xmind.topicShape.ellipse",
                "arrow-end-class": "inherited",
            },
        },
        "importantTopic": {
            "id": topic_id("theme.importantTopic"),
            "properties": {
                "svg:fill": "#EA580C",
                "fill-pattern": "solid",
                "border-line-color": "#EA580C",
            },
        },
        "minorTopic": {
            "id": topic_id("theme.minorTopic"),
            "properties": {
                "svg:fill": "#F2B807",
                "fill-pattern": "solid",
                "border-line-color": "#F2B807",
            },
        },
        "expiredTopic": {
            "id": topic_id("theme.expiredTopic"),
            "properties": {
                "fo:text-decoration": "line-through",
                "fill-pattern": "none",
            },
        },
        "boundary": {
            "id": topic_id("theme.boundary"),
            "properties": {
                **common_text,
                "fo:font-size": "14pt",
                "fo:font-weight": "600",
                "fo:text-align": "center",
                "svg:fill": "#2563EB",
                "fill-pattern": "solid",
                "line-width": "2",
                "line-color": "#2563EB",
                "line-pattern": "dash",
                "shape-class": "org.xmind.boundaryShape.roundedRect",
            },
        },
        "summary": {
            "id": topic_id("theme.summary"),
            "properties": {
                "line-width": "2pt",
                "line-color": "#2563EB",
                "line-pattern": "solid",
                "shape-class": "org.xmind.summaryShape.square",
            },
        },
        "relationship": {
            "id": topic_id("theme.relationship"),
            "properties": {
                **common_text,
                "fo:font-size": "13pt",
                "fo:font-weight": "600",
                "fo:text-align": "center",
                "line-width": "2",
                "line-color": "#2563EB",
                "line-pattern": "dash",
                "shape-class": "org.xmind.relationshipShape.curved",
                "arrow-begin-class": "org.xmind.arrowShape.none",
                "arrow-end-class": "org.xmind.arrowShape.triangle",
            },
        },
        "skeletonThemeId": "a148ee55687bdfc44af2fa5f16",
        "colorThemeId": "AI-KE-BASE",
    }


def build_content_json(root: Topic) -> str:
    sheet = {
        "id": topic_id("sheet"),
        "revisionId": topic_id("revision"),
        "class": "sheet",
        "rootTopic": topic_to_json(root, "root"),
        "relationships": [],
        "title": "逻辑图",
        "topicOverlapping": "overlap",
        "arrangeableLayerOrder": first_layer_ids(root),
        "zones": [],
        "extensions": [
            {
                "provider": "org.xmind.ui.skeleton.structure.style",
                "content": {"centralTopic": "org.xmind.ui.logic.right"},
            }
        ],
        "theme": build_theme(),
    }
    return json.dumps([sheet], ensure_ascii=False, separators=(",", ":"))


def build_manifest_json() -> str:
    return json.dumps(
        {
            "file-entries": {
                "content.json": {},
                "metadata.json": {},
                "Thumbnails/thumbnail.png": {},
            }
        },
        ensure_ascii=False,
        separators=(",", ":"),
    )


def build_metadata_json(root: Topic) -> str:
    return json.dumps(
        {
            "dataStructureVersion": "3",
            "layoutEngineVersion": "5",
            "creator": {"name": "Vana", "version": "26.02.04171"},
        },
        ensure_ascii=False,
        separators=(",", ":"),
    )


def write_xmind(path: Path, root: Topic) -> None:
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_STORED) as zf:
        zf.writestr("content.json", build_content_json(root))
        zf.writestr("metadata.json", build_metadata_json(root))
        zf.writestr("Thumbnails/", b"")
        zf.writestr("Thumbnails/thumbnail.png", PNG_1X1)
        zf.writestr("manifest.json", build_manifest_json())
        zf.writestr("content.xml", build_legacy_content_xml(root))


def count_json_topics(topic: dict) -> int:
    total = 1
    for child in topic.get("children", {}).get("attached", []):
        total += count_json_topics(child)
    for child in topic.get("children", {}).get("detached", []):
        total += count_json_topics(child)
    return total


def validate_xmind(path: Path) -> dict:
    with zipfile.ZipFile(path) as zf:
        bad_file = zf.testzip()
        names = set(zf.namelist())
        required = {
            "content.json",
            "metadata.json",
            "Thumbnails/thumbnail.png",
            "manifest.json",
            "content.xml",
        }
        missing = sorted(required - names)
        content_json = json.loads(zf.read("content.json").decode("utf-8"))
        metadata = json.loads(zf.read("metadata.json").decode("utf-8"))
        manifest = json.loads(zf.read("manifest.json").decode("utf-8"))
        png = zf.read("Thumbnails/thumbnail.png")
        content_xml = zf.read("content.xml")

    content_root = ET.fromstring(content_xml)
    ns = {"x": "urn:xmind:xmap:xmlns:content:2.0"}
    xml_root_title = content_root.findtext("./x:sheet/x:topic/x:title", namespaces=ns)
    sheet = content_json[0]
    root_topic = sheet["rootTopic"]
    return {
        "path": str(path),
        "bad_file": bad_file,
        "missing": missing,
        "json_root_title": root_topic["title"],
        "xml_root_title": xml_root_title,
        "json_topic_count": count_json_topics(root_topic),
        "dataStructureVersion": metadata.get("dataStructureVersion"),
        "layoutEngineVersion": metadata.get("layoutEngineVersion"),
        "manifest_entries": list(manifest.get("file-entries", {}).keys()),
        "thumbnail_png": png.startswith(b"\x89PNG\r\n\x1a\n"),
    }


def main() -> None:
    write_xmind(PRIMARY_XMIND, MINDMAP)
    write_xmind(XMIND8_XMIND, MINDMAP)
    write_xmind(JSON_FALLBACK_XMIND, MINDMAP)

    results = [
        validate_xmind(PRIMARY_XMIND),
        validate_xmind(XMIND8_XMIND),
        validate_xmind(JSON_FALLBACK_XMIND),
    ]
    print(json.dumps(results, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
