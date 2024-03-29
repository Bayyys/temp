import React, { useCallback, useEffect, useRef, useState } from "react";
import { Card, Form, Input, Cascader, Button, message } from "antd";
import { ArrowLeftOutlined } from "@ant-design/icons";
import { useLocation, useNavigate } from "react-router-dom";
import { useForm } from "antd/es/form/Form";
import ImgUpload from "./ImgUpload";
import { reqCategorys, reqAddOrUpdateProduct } from "../../api/api";
import RichTextEditor from "./RichTextEditor";

const { Item } = Form;
const { TextArea } = Input;

// 产品的添加和更新的路由组件
export default function ProductAddUpdate() {
  const [cascaderOptions, setCascaderOptions] = useState([]);
  const navigate = useNavigate();
  const [form] = useForm();
  const pIdsRef = useRef([]);

  const {
    state: { product },
  } = useLocation();
  const { pCategoryId, categoryId } = product;

  const addOrUpdate = async (product) => {
    try {
      const result = await reqAddOrUpdateProduct(product);
      if (result.status === 0) {
        message.success(`${product._id ? "更新" : "添加"}商品成功`);
        navigate(-1);
      } else {
        message.error(`${product._id ? "更新" : "添加"}商品失败`);
      }
    } catch (error) {
      message.error(`${product._id ? "更新" : "添加"}商品失败`);
    }
  };

  const validateForm = () => {
    form
      .validateFields()
      .then((values) => {
        const { name, desc, price, category, imgs, detail } = values;
        let pCategoryId, categoryId;
        if (category.length === 1) {
          pCategoryId = "0";
          categoryId = category[0];
        } else {
          pCategoryId = category[0];
          categoryId = category[1];
        }
        const nProduct = {
          // 新的 product
          ...product,
          name,
          desc,
          price,
          pCategoryId,
          categoryId,
          imgs,
          detail,
        };
        if (product._id) {
          // 若更新, 需要添加 _id
          nProduct._id = product._id;
        }
        addOrUpdate(nProduct);
      })
      .catch((errorInfo) => {
        message.error("表单验证失败");
      });
  };

  const getChildCategorys = useCallback(async (parentId) => {
    try {
      const result = await reqCategorys(parentId);
      if (result.status === 0) {
        return result.data;
      }
    } catch (error) {}
  }, []);

  const initCategorys = useCallback(
    async (categorys) => {
      const options = categorys.map((item) => ({
        value: item._id,
        label: item.name,
        isLeaf: false,
      }));

      if (pCategoryId !== "0") {
        const subCategorys = await getChildCategorys(pCategoryId);
        const childOptions = subCategorys.map((item) => ({
          value: item._id,
          label: item.name,
          isLeaf: true,
        }));
        options.forEach((item) => {
          if (item.value === pCategoryId) {
            item.children = childOptions;
            return;
          }
        });
      }
      setCascaderOptions(options);
    },
    [getChildCategorys, pCategoryId]
  );

  const getFirstCategorys = useCallback(
    async (parentId) => {
      try {
        const result = await reqCategorys(parentId);
        if (result.status === 0) {
          const categorys = result.data;
          initCategorys(categorys);
        }
      } catch (error) {}
    },
    [initCategorys]
  );

  const loadData = async (selectedOptions) => {
    const targetOption = selectedOptions[selectedOptions.length - 1];
    try {
      const result = await getChildCategorys(targetOption.value);
      if (result && result.length > 0) {
        targetOption.children = result.map((item) => ({
          value: item._id,
          label: item.name,
          isLeaf: true,
        }));
      } else {
        targetOption.isLeaf = true;
      }
    } catch (error) {
      message.error("加载数据失败");
    }
    setCascaderOptions([...cascaderOptions]);
  };

  const initpid = useCallback(() => {
    // 清空 pIDs
    pIdsRef.current.length = 0;
    if (pCategoryId === "0") {
      pIdsRef.current.push(categoryId);
    } else {
      pIdsRef.current.push(pCategoryId);
      pIdsRef.current.push(categoryId);
    }
  }, [categoryId, pCategoryId]);

  const normFile = (e) => {
    return e
      ?.filter((item) => item.name !== "error.jpg")
      .map((item) => item.name);
  };

  const title = (
    <span>
      <Button
        type="link"
        icon={<ArrowLeftOutlined />}
        onClick={() => {
          navigate(-1);
        }}
      ></Button>
      <span>{product.name ? "修改商品" : "添加商品"}</span>
    </span>
  );

  const formItemLayout = {
    labelCol: { span: 3 }, // 左侧 label 的宽度
    labelAlign: "left", // label 文字对齐方式
    wrapperCol: { span: 8 }, // 右侧包裹的宽度
  };

  useEffect(() => {
    getFirstCategorys("0");
    initpid();
  }, [getFirstCategorys, initpid]);

  return (
    <Card title={title}>
      <Form
        {...formItemLayout}
        form={form}
        validateTrigger="onBlur"
        initialValues={product}
      >
        <Item
          label="商品名称"
          name="name"
          rules={[{ required: true, message: "商品名称必须输入" }]}
          validateFirst
          hasFeedback
        >
          <Input placeholder="请输入商品名称" allowClear />
        </Item>
        <Item label="商品描述" name="desc" wrapperCol={{ span: 15 }}>
          <TextArea
            placeholder="请输入商品描述"
            autoSize={{ minRows: 3 }}
            showCount
            maxLength={100}
          />
        </Item>
        <Item
          label="商品价格"
          name="price"
          rules={[
            {
              required: true,
              message: "商品价格必须输入",
            },
            {
              validator: (_, value) => {
                if (value <= 0) {
                  return Promise.reject(new Error("价格必须大于 0"));
                } else if (value >= 999999) {
                  return Promise.reject(new Error("价格必须小于 999999"));
                } else {
                  return Promise.resolve();
                }
              },
            },
          ]}
          validateFirst
          hasFeedback
        >
          <Input type="number" addonAfter="元" />
        </Item>
        <Item
          label="商品分类"
          name="category"
          rules={[
            {
              required: true,
              message: "商品分类必须选择",
            },
          ]}
          initialValue={pIdsRef.current}
        >
          <Cascader
            options={cascaderOptions}
            loadData={loadData}
            placeholder="请选择商品分类"
          />
        </Item>
        <Item
          label="商品图片"
          name="imgs"
          valuePropName="fileList"
          getValueFromEvent={normFile}
        >
          <ImgUpload imgs={product.imgs} />
        </Item>
        <Item label="商品详情" name="detail" wrapperCol={{ span: 20 }}>
          <RichTextEditor placeholder="请填写商品详情信息" />
        </Item>
        <Item>
          <Button
            type="primary"
            onClick={() => {
              validateForm();
            }}
          >
            提交
          </Button>
        </Item>
      </Form>
    </Card>
  );
}
