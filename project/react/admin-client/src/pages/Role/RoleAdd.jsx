import React from "react";
import { Modal, Form, Input, Spin } from "antd";
const { Item } = Form;

export default function RoleAdd({ open, setOpen, addRole }) {
  const [form] = Form.useForm();
  const [loading, setLoading] = React.useState(false);

  const handleAddOk = async (form) => {
    setLoading(true);
    try {
      const result = await form.validateFields();
      if (result) {
        addRole(result.name);
        setOpen(false);
      }
    } catch (error) {}
    setLoading(false);
  };

  return (
    <Modal
      destroyOnClose={true}
      open={open}
      onCancel={() => {
        setOpen(false);
      }}
      onOk={() => handleAddOk(form)}
      title="添加角色"
    >
      <Spin spinning={loading}>
        <Form form={form} preserve={false}>
          <Item
            label="角色名称"
            name="name"
            rules={[{ required: true, message: "角色名称不能为空" }]}
          >
            <Input placeholder="请输入角色名称"></Input>
          </Item>
        </Form>
      </Spin>
    </Modal>
  );
}
