from langchain_openai import ChatOpenAI


def qianwen_llm():
    """
    实验室通义千问32B
    """
    model = "/nfs01/projects/50501243/s120212227183/code/qwen-1.5-32b/Qwen1.5-32B-Chat"
    temperature = 0.7
    api_key = "EMPTY"
    base_url = "http://fushi.menglangpoem.cn:8099/v1"
    llm = ChatOpenAI(model=model, temperature=temperature, api_key=api_key, base_url=base_url, max_tokens=2048)
    return llm


if __name__ == '__main__':
    llm = qianwen_llm()
    input = '''
    """  您是一名文本分类专家，请根据所提供的文本内容和提供的分类，对文本进行分类。分类的规则如下：
                    {{
                    "rule_id": "匹配的分类ID",
                    "rule_type": "匹配的分类",
                    "text": "所提供的进行分类的文本内容。",
                    "reason": "请提供一个合理的理由，解释为什么该文本应归类为这个分类。"
                    }}
                    如果文块不能与所提供的分类匹配，则将 rule_id 的值设置为 -1。
                    请注意，您的回答应清晰、准确，并提供充分的细节来支持您的分类。同时，您可以使用所提供的分类和其他相关信息来解释您的决策。让我们一步一步来思考
    <文本>   
    6. 材料和工程设备\n6.1 承包人提供的材料和工程设备\n6.1.1 除专用合同条款另有约定外,承包人提供的材料和工程设备均由承包人负责采购､运输和保管｡承包人应对其采购的材料和工程设备负责｡应由承包人提供的设备在专用条款中约定｡\n6.1.2 承包人应按专用合同条款的约定,将各项材料和工程设备的供货人及品种､技术要求､规格､数量和供货时间等报送发包人批准｡承包人应向发包人提交其负责提供的材料和工程设备的质量证明文件,并满足合同约定的质量标准｡\n6.1.3 对承包人提供的材料和工程设备,承包人应会同发包人进行检验和交货验收,查验材料合格证明和产品合格证书,并按合同约定和发包人指示,进行材料的抽样检验和工程设备的检验测试,检验和测试结果应提交发包人,所需费用由承包人承担｡\n6.1.4承包人提供的永久性工程的材料和部件\n承包人依据设计文件规定的技术参数､技术条件､功能要求和使用要求,负责组织永久性工程的材料､部件的采购的､负责运抵现场,并对其质量检查结果和性能结果负责｡\n因承包人提供的材料､部件(包括建筑构件等)不符合国家强制性标准规定所造成的质量缺陷,由承包人自费修复缺陷,因此造成进度延误的,竣工日期不予延长｡\n6.1.5主要材料承包人须选择一线品牌的名优产品｡\n6.2 发包人提供的材料和工程设备\n6.2.1 专用合同条款约定发包人提供的部分材料和工程设备｡\n6.2.2承包人应根据合同进度计划的安排,向发包人报送要求发包人交货的日期计划｡发包人应按照合同双方当事人商定的交货日期,向承包人提交材料和工程设备｡\n6.2.3发包人应在材料和工程设备到货前通知承包人,承包人应会同发包人在约定的时间内,赴交货地点共同进行验收｡除专用合同条款另有约定外,发包人提供的材料和工程设备验收后,由承包人负责接收､运输和保管｡\n6.2.4发包人要求向承包人提前交货的,承包人不得拒绝｡\n6.2.5承包人要求更改交货日期或地点的,应事先报请发包人批准｡由于承包人要求更改交货时间或地点所增加的费用和(或)工期延误由承包人承担｡\n6.2.6发包人提供的材料和工程设备的规格､数量或质量不符合合同要求,或由于发包人原因发生交货日期延误及交货地点变更等情况的,发包人应承担由此增加的费用和(或)工期延误｡\n6.3 专用于工程的材料和工程设备\n6.3.1 运入施工场地的材料､工程设备,包括备品备件､安装专用工器具与随机资料,必须专用于合同约定范围内的工程,未经发包人同意,承包人不得运出施工场地或挪作他用｡\n6.3.2 随同工程设备运入施工场地的备品备件､专用工器具与随机资料,应由承包人会同发包人按供货人的装箱单清点后共同封存,未经发包人同意不得启用｡承包人因合同工作需要使用上述物品时,应向发包人提出申请｡\n6.4 实施方法\n承包人对材料的加工､制造､安装应当按照法律规定､合同约定以及行业习惯来实施｡\n对于承包单位(或分包单位)私自降低标准的设备､施工,发包人可以要求给予更换及整改,或者按1-3倍市场价格的在工程结算中扣除｡\n承包人应按照附件六《建设工程安全文明环境管理协议》的要求组织施工,确保施工安全｡\n6.5 禁止使用不合格的材料和工程设备\n6.5.1发包人有权拒绝承包人提供的不合格材料或工程设备,并要求承包人立即进行更换｡发包人应在更换后再次进行检查和检验,由此增加的费用和(或)工期延误由承包人承担｡\n6.5.2发包人发现承包人使用了不合格的材料和工程设备,应即时发出指示要求承包人立即改正,并禁止在工程中继续使用不合格的材料和工程设备｡\n6.5.3 发包人提供的材料或工程设备不符合合同要求的,承包人有权拒绝,并可要求发包人更换,由此增加的费用和(或)工期延误由发包人承担｡\n6.5.4非发包人原因,发生的设备及材料代用,必须经发包人书面批准,并下发正式变更指令后,承包人方可实施,由此而增加的工程量及费用由承包人承担;由此减少的工程量及费用由发包人从承包人合同价格中扣减｡\n6.6 工程物资保管与剩余\n6.6.1工程物资保管\n发包人已采购的设备(包括业主及上海康恒环境股份有限公司采购的设备和材料),标段一承包人､发包人共同进行质量验收后由标段一承包人接收,标段一承包人负责设备的卸车､倒运､保管(包括吊车进出厂､台班使用费､地基处理､吊装措施费用及现场施工用脚手架等)｡项目所需的全部发包人已采购的设备均由标段一承包人保管(有关代保管管理要求详见附件八中《甲供设备材料代保管管理规定》),所需的一切费用,包含在中标合同价格内｡提交工程物资保管､维护方案的时间在专用条款1.6.1中约定｡\n6.6.2剩余工程物资的移交\n承包人为永久性工程保管的物资,在工程竣工后,剩余的工程物资无偿移交给发包人｡\n
    </文本>
    <分类>
    1.合同价格
    2.违约条款
    3.履约保函
    4.质保金
    5.结算价格
    </分类>
    '''
    chain = llm
    result = llm.invoke(input)
    print(result)
