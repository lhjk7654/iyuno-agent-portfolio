import streamlit as st

from app.agent import run_agent


st.set_page_config(
    page_title="Iyuno AI Security Agent",
    page_icon="🔐",
    layout="wide",
)


st.title("🔐 Iyuno AI Security Agent")

st.write(
    "NIST AI 및 Cybersecurity 문서를 기반으로 "
    "Tool Calling을 수행하는 AI Agent입니다."
)

st.divider()


question = st.text_input(
    "질문을 입력하세요",
    placeholder="What are the characteristics of trustworthy AI?",
)


if st.button("Ask", type="primary"):

    if not question.strip():
        st.warning("질문을 입력해주세요.")

    else:
        with st.spinner("Agent is searching documents and generating an answer..."):

            result = run_agent(question)

        st.subheader("Answer")

        st.write(result["answer"])


        st.subheader("Agent Information")

        col1, col2 = st.columns(2)

        with col1:
            if result["tool_used"]:
                st.success("🔧 Tool Calling Used")
            else:
                st.info("No Tool Calling")

        with col2:
            st.metric(
                "Tools Used",
                len(result["tool_results"]),
            )


        if result["tool_results"]:

            st.subheader("Retrieved Sources")

            for tool_result in result["tool_results"]:

                for i, item in enumerate(
                    tool_result["results"],
                    start=1,
                ):

                    with st.expander(
                        f"{i}. {item['source']} "
                        f"(chunk {item['chunk']})"
                    ):

                        st.write(
                            f"Distance: {item['distance']:.4f}"
                        )

                        st.write(item["text"])