import { stringify } from "query-string";
import { fetchUtils, DataProvider } from "ra-core";

const countHeader: string = "Content-Range";

export const getApiBaseUrl = () => window["env"]["backendUrl"];

export const createClient = (url: any, options: any = {}) => {
  return fetchUtils.fetchJson(url, options);
};

export const createAuthenticatedClient = (
  url: any,
  options: any = {},
  token: string
) => {
  options.user = {
    authenticated: true,
    token: `Bearer ${token}`,
  };
  return fetchUtils.fetchJson(url, options);
};

export default (getAccessTokenSilently: () => Promise<any>): DataProvider => ({
  getList: async (resource, params) => {
    const { page, perPage } = params.pagination;
    const { field, order } = params.sort;

    const rangeStart = (page - 1) * perPage;
    const rangeEnd = page * perPage - 1;

    const query = {
      sort: JSON.stringify([field, order]),
      range: JSON.stringify([rangeStart, rangeEnd]),
      filter: JSON.stringify(params.filter),
    };
    const url = `${getApiBaseUrl()}/${resource}?${stringify(query)}`;
    const options =
      countHeader === "Content-Range"
        ? {
            // Chrome doesn't return `Content-Range` header if no `Range` is provided in the request.
            headers: new Headers({
              Range: `${resource}=${rangeStart}-${rangeEnd}`,
            }),
          }
        : {};

    const token = await getAccessTokenSilently();
    return createAuthenticatedClient(url, options, token).then(
      ({ headers, json }) => {
        let total = 0;
        if (headers.has(countHeader)) {
          total =
            countHeader === "Content-Range"
              ? parseInt(headers.get("content-range")!.split("/").pop()!, 10)
              : parseInt(headers.get(countHeader.toLowerCase())!);
        } else {
          total = json[resource].length;
        }
        return {
          data: json[resource],
          total: total,
        };
      }
    );
  },

  getOne: async (resource, params) => {
    //Replaces forwardslash by "Forwardslash" to be able to use uri's as id
    const token = await getAccessTokenSilently();
    return createAuthenticatedClient(
      `${getApiBaseUrl()}/${resource}/${encodeURIComponent(
        params.id.toString().replace(/\//g, "Forwardslash")
      )}`,
      {},
      token
    ).then(({ json }) => ({
      data: json,
    }));
  },

  getMany: async (resource, params) => {
    const query = {
      filter: JSON.stringify({ id: params.ids }),
    };
    const url = `${getApiBaseUrl()}/${resource}?${stringify(query)}`;
    const token = await getAccessTokenSilently();
    return createAuthenticatedClient(url, {}, token).then(({ json }) => ({
      data: json[resource],
    }));
  },

  getManyReference: async (resource, params) => {
    const { page, perPage } = params.pagination;
    const { field, order } = params.sort;

    const rangeStart = (page - 1) * perPage;
    const rangeEnd = page * perPage - 1;

    params.filter[params.target] = params.id;

    const query = {
      sort: JSON.stringify([field, order]),
      range: JSON.stringify([rangeStart, rangeEnd]),
      filter: JSON.stringify(params.filter),
    };
    const url = `${getApiBaseUrl()}/${resource}?${stringify(query)}`;

    const token = await getAccessTokenSilently();
    return createAuthenticatedClient(url, {}, token).then(
      ({ headers, json }) => {
        let total = 0;
        if (headers.has(countHeader)) {
          total =
            countHeader === "Content-Range"
              ? parseInt(headers.get("content-range")!.split("/").pop()!, 10)
              : parseInt(headers.get(countHeader.toLowerCase())!);
        } else {
          total = json[resource].length;
        }
        return {
          data: json[resource],
          total: total,
        };
      }
    );
  },

  update: async (resource, params) => {
    const token = await getAccessTokenSilently();
    return createAuthenticatedClient(
      `${getApiBaseUrl()}/${resource}/${params.id}`,
      {
        method: "PUT",
        body: JSON.stringify(params.data),
      },
      token
    ).then(({ json }) => ({ data: json }));
  },

  // simple-rest doesn't handle provide an updateMany route, so we fallback to calling update n times instead
  updateMany: async (resource, params) => {
    const token = await getAccessTokenSilently();
    return Promise.all(
      params.ids.map((id) =>
        createAuthenticatedClient(
          `${getApiBaseUrl()}/${resource}/${id}`,
          {
            method: "PUT",
            body: JSON.stringify(params.data),
          },
          token
        )
      )
    ).then((responses) => ({ data: responses.map(({ json }) => json.id) }));
  },
  create: async (resource, params) => {
    const token = await getAccessTokenSilently();
    if (resource === "documents" && (params as any).data.files) {
      if ((params as any).data.files.length > 10) {
        throw new Error("You can only upload max 10 documents at a time.");
      }
      let allUploads = Promise.all(
        (params as any).data.files.map((file: any) => {
          const formData = new FormData();
          formData.append("file", file.rawFile);
          return createAuthenticatedClient(
            `${getApiBaseUrl()}/${resource}/file`,
            {
              method: "POST",
              body: formData,
            },
            token
          );
        })
      );

      return allUploads.then((responseArray: any[]) => {
        return {
          data: responseArray[0].json,
        };
      });
    }

    return createAuthenticatedClient(
      `${getApiBaseUrl()}/${resource}`,
      {
        method: "POST",
        body: JSON.stringify(params.data),
      },
      token
    ).then(({ json }) => {
      return {
        data: json,
      };
    });
  },
  delete: async (resource, params) => {
    const token = await getAccessTokenSilently();
    return createAuthenticatedClient(
      `${getApiBaseUrl()}/${resource}/${params.id}`,
      {
        method: "DELETE",
        headers: new Headers({
          "Content-Type": "text/plain",
        }),
      },
      token
    ).then(({ json }) => ({ data: json }));
  },
  // simple-rest doesn't handle filters on DELETE route, so we fallback to calling DELETE n times instead
  deleteMany: async (resource, params) => {
    const token = await getAccessTokenSilently();
    return Promise.all(
      params.ids.map((id) =>
        createAuthenticatedClient(
          `${getApiBaseUrl()}/${resource}/${id}`,
          {
            method: "DELETE",
            headers: new Headers({
              "Content-Type": "text/plain",
            }),
          },
          token
        )
      )
    ).then((responses) => ({
      data: responses.map(({ json }) => json),
    }));
  },
});
