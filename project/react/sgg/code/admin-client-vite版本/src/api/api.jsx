/*
要求: 能根据接口文档定义接口请求
包含应用中所有接口请求函数的模块
每个函数的返回值都是promise

基本要求: 能根据接口文档定义接口请求函数
 */
import ajax from "./ajax";

/* ----- 百度地图 api ----- */
// jsonp请求的接口请求函数
export const getRegionCode = async (city) => {
  try {
    const res = await ajax(BASE + "/region", { city: city }, "GET");
    if (res.status === 0) {
      if (res.result_size === 0) {
        return "unknown_city";
      }
      return res.districts[0].code;
    } else {
      return "error";
    }
  } catch (error) {
    return "error";
  }
};

export const getCity = async () => {
  try {
    const res = await ajax(BASE + "/city", {}, "GET");
    if (res.status === 0) {
      if (!res.content) {
        return "unknown_city";
      }
      return res.content.address_detail.adcode;
    } else {
      return "error";
    }
  } catch (error) {
    return "error";
  }
};

export const getWeather = async (city) => {
  try {
    let code = "000";
    if (!city) {
      code = await getCity();
      if (code === "error") {
        return Promise.reject("定位错误");
      }
      if (code === "unknown_city") {
        return Promise.reject("未知城市");
      }
    } else {
      code = await getRegionCode(city);
      if (code === "error") {
        return Promise.reject("定位错误");
      }
      if (code === "unknown_city") {
        return Promise.reject("未知城市");
      }
    }
    const res = await ajax(BASE + "/weather", { code }, "GET");
    if (res.status === 0 && res.message === "success") {
      return Promise.resolve({
        weather: res.result.now.text,
        city: res.result.location.name,
      });
    } else {
      return Promise.reject("未知城市");
    }
  } catch (error) {
    return Promise.reject("定位错误或城市数据缺失");
  }
};

/* ----- 后台请求信息 ----- */

const BASE = "/api";

// 登陆
export const reqLogin = (username, password) =>
  ajax(BASE + "/login", { username, password }, "POST");

// 添加用户
export const reqAddUser = (user) =>
  ajax(BASE + "/manage/user/add", user, "POST");

// 获取一级/二级分类的列表
export const reqCategorys = (parentId) =>
  ajax(BASE + "/manage/category/list", { parentId });

// 添加分类
export const reqAddCategory = (categoryName, parentId) =>
  ajax(BASE + "/manage/category/add", { categoryName, parentId }, "POST");

// 更新分类
export const reqUpdateCategory = ({ categoryId, categoryName }) =>
  ajax(BASE + "/manage/category/update", { categoryId, categoryName }, "POST");

// 获取一个分类
export const reqCategory = (categoryId) =>
  ajax(BASE + "/manage/category/info", { categoryId });

// 获取商品分页列表
export const reqProducts = (pageNum, pageSize) =>
  ajax(BASE + "/manage/product/list", { pageNum, pageSize });

// 更新商品的状态(上架/下架)
export const reqUpdateStatus = (productId, status) =>
  ajax(BASE + "/manage/product/updateStatus", { productId, status }, "POST");

/*
搜索商品分页列表 (根据商品名称/商品描述)
searchType: 搜索的类型, productName/productDesc
 */
export const reqSearchProducts = (pageNum, pageSize, searchName, searchType) =>
  ajax(BASE + "/manage/product/search", {
    pageNum,
    pageSize,
    [searchType]: searchName,
  });

// 搜索商品分页列表 (根据商品描述)
/*export const reqSearchProducts2 = ({pageNum, pageSize, searchName}) => ajax(BASE + '/manage/product/search', {
  pageNum,
  pageSize,
  productDesc: searchName,
})*/

// 删除指定名称的图片
export const reqDeleteImg = (name) =>
  ajax(BASE + "/manage/img/delete", { name }, "POST");

// 添加/修改商品
export const reqAddOrUpdateProduct = (product) =>
  ajax(
    BASE + "/manage/product/" + (product._id ? "update" : "add"),
    product,
    "POST"
  );
// 修改商品
// export const reqUpdateProduct = (product) => ajax(BASE + '/manage/product/update', product, 'POST')

// 获取所有角色的列表
export const reqRoles = () => ajax(BASE + "/manage/role/list");
// 添加角色
export const reqAddRole = (roleName) =>
  ajax(BASE + "/manage/role/add", { roleName }, "POST");
// 添加角色
export const reqUpdateRole = (role) =>
  ajax(BASE + "/manage/role/update", role, "POST");

// 获取所有用户的列表
export const reqUsers = () => ajax(BASE + "/manage/user/list");
// 删除指定用户
export const reqDeleteUser = (userId) =>
  ajax(BASE + "/manage/user/delete", { userId }, "POST");
// 添加/更新用户
export const reqAddOrUpdateUser = (user) =>
  ajax(BASE + "/manage/user/" + (user._id ? "update" : "add"), user, "POST");
