# (C) 2021 GoodData Corporation
from __future__ import annotations
from typing import Union, Dict, Set, List
import functools
import gooddata_metadata_client.apis as metadata_apis
import gooddata_afm_client.apis as afm_apis
import gooddata_afm_client.models as afm_models
from gooddata_sdk.utils import Sideloads, id_obj_to_key, load_all_entities
from gooddata_sdk.client import GoodDataApiClient
from gooddata_sdk.compute import ExecutionDefinition
from gooddata_sdk.compute_model import (
    Attribute,
    SimpleMetric,
    ObjId,
    Metric,
    Filter,
    compute_model_to_api_model,
)

# need to use types from typings here for Python <3.9
ValidObjects = Dict[str, Set[str]]


class CatalogEntry:
    @property
    def id(self) -> str:
        raise NotImplementedError()

    @property
    def type(self) -> str:
        raise NotImplementedError()

    @property
    def obj_id(self) -> ObjId:
        raise NotImplementedError()

    @property
    def title(self) -> str:
        raise NotImplementedError()

    @property
    def description(self) -> str:
        raise NotImplementedError()


class CatalogLabel(CatalogEntry):
    def __init__(self, label):
        super(CatalogLabel, self).__init__()

        self._l = label["attributes"]
        self._label = label
        self._obj_id = ObjId(self._label["id"], type=self._label["type"])

    @property
    def id(self) -> str:
        return self._label["id"]

    @property
    def type(self) -> str:
        return self._label["type"]

    @property
    def title(self) -> str:
        return self._label["type"]

    @property
    def obj_id(self) -> ObjId:
        return self._obj_id

    @property
    def description(self) -> str:
        return self._l["description"]

    @property
    def primary(self) -> bool:
        return "primary" in self._l and self._l["primary"]

    def as_computable(self) -> Attribute:
        return Attribute(local_id=self.id, label=self.id)

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return f"CatalogLabel(id={self.id}, title={self.title})"


class CatalogAttribute(CatalogEntry):
    def __init__(self, attribute, labels: list[CatalogLabel]):
        super(CatalogAttribute, self).__init__()

        self._a = attribute["attributes"]
        self._attribute = attribute
        self._labels = labels
        self._labels_idx = dict([(str(label.obj_id), label) for label in labels])
        self._obj_id = ObjId(self._attribute["id"], self._attribute["type"])

    @property
    def id(self) -> str:
        return self._attribute["id"]

    @property
    def type(self) -> str:
        return self._attribute["type"]

    @property
    def obj_id(self) -> ObjId:
        return self._obj_id

    @property
    def title(self) -> str:
        return self._a["title"]

    @property
    def description(self) -> str:
        return self._a["description"]

    @property
    def labels(self) -> list[CatalogLabel]:
        return self._labels

    @property
    def granularity(self) -> Union[str, None]:
        return self._a["granularity"] if "granularity" in self._a else None

    def primary_label(self) -> CatalogLabel:
        return next(filter(lambda l: l.primary, self.labels), None)

    def find_label(self, id_obj) -> Union[CatalogLabel, None]:
        obj_key = id_obj_to_key(id_obj)

        return self._labels_idx[obj_key] if obj_key in self._labels_idx else None

    def as_computable(self) -> Attribute:
        primary_label = self.primary_label()

        if primary_label is not None:
            return primary_label.as_computable()

        # cannot even write meaningful error here. cannot create attribute from attribute? :D
        raise ValueError()

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return (
            f"CatalogAttribute(id={self.id}, title={self.title}, labels={self.labels})"
        )


class CatalogFact(CatalogEntry):
    def __init__(self, fact):
        super(CatalogFact, self).__init__()

        self._f = fact["attributes"]
        self._fact = fact
        self._obj_id = ObjId(self._fact["id"], self._fact["type"])

    @property
    def id(self) -> str:
        return self._fact["id"]

    @property
    def type(self) -> str:
        return self._fact["type"]

    @property
    def obj_id(self) -> ObjId:
        return self._obj_id

    @property
    def title(self) -> str:
        return self._f["title"]

    @property
    def description(self) -> str:
        return self._f["description"]

    def as_computable(self) -> Metric:
        return SimpleMetric(local_id=self.id, item=ObjId(self.id, "fact"))

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return f"CatalogFact(id={self.id}, title={self.title})"


class CatalogMetric(CatalogEntry):
    def __init__(self, metric):
        super(CatalogMetric, self).__init__()

        self._m = metric["attributes"]
        self._metric = metric
        self._obj_id = ObjId(self._metric["id"], self._metric["type"])

    @property
    def id(self) -> str:
        return self._metric["id"]

    @property
    def type(self) -> str:
        return self._metric["type"]

    @property
    def obj_id(self) -> ObjId:
        return self._obj_id

    @property
    def title(self) -> str:
        return self._m["title"]

    @property
    def description(self) -> str:
        return self._m["description"]

    def as_computable(self) -> Metric:
        return SimpleMetric(local_id=self.id, item=ObjId(self.id, "metric"))

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return f"CatalogMetric(id={self.id}, title={self.title})"


class CatalogDataset(CatalogEntry):
    def __init__(self, dataset, attributes, facts):
        super(CatalogDataset, self).__init__()

        self._d = dataset["attributes"]
        self._dataset = dataset
        self._attributes = attributes
        self._facts = facts
        self._obj_id = ObjId(self._dataset["id"], self._dataset["type"])

    @property
    def id(self) -> str:
        return self._dataset["id"]

    @property
    def type(self) -> str:
        return self._dataset["type"]

    @property
    def obj_id(self) -> ObjId:
        return self._obj_id

    @property
    def title(self) -> str:
        return self._d["title"]

    @property
    def description(self) -> str:
        return self._d["description"]

    @property
    def attributes(self) -> list[CatalogAttribute]:
        return self._attributes

    @property
    def facts(self) -> list[CatalogFact]:
        return self._facts

    def find_label_attribute(self, id_obj) -> Union[CatalogAttribute, None]:
        for attr in self._attributes:
            if attr.find_label(id_obj) is not None:
                return attr

        return None

    def filter_dataset(self, valid_objects: ValidObjects):
        """
        Filters dataset so that it contains only attributes and facts that are part of the provided valid objects
        structure.

        :param valid_objects: mapping of object type to a set of valid object ids
        :return: CatalogDataset containing only valid attributes and facts; None if all of the attributes and facts were filtered out
        """
        new_attributes = [a for a in self.attributes if a.id in valid_objects[a.type]]
        new_facts = [f for f in self.facts if f.id in valid_objects[f.type]]

        if not len(new_attributes) and not len(new_facts):
            return None

        return CatalogDataset(self._dataset, new_attributes, new_facts)

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return f"CatalogDataset(id={self.id}, title={self.title}, facts={self.facts}, attributes={self.attributes})"


ValidObjectTypes = Union[
    Attribute, Metric, Filter, CatalogLabel, CatalogFact, CatalogMetric
]

# need to use types from typings here for Python <3.9
ValidObjectsInputType = Union[
    ValidObjectTypes, List[ValidObjectTypes], ExecutionDefinition
]


class Catalog:
    def __init__(
        self,
        valid_obj_fun,
        datasets: list[CatalogDataset],
        metrics: list[CatalogMetric],
    ):
        self._valid_obf_fun = valid_obj_fun
        self._datasets = datasets
        self._metrics = metrics
        self._metric_idx = dict([(str(m.obj_id), m) for m in metrics])
        self._datasets_idx = dict([(str(d.obj_id), d) for d in datasets])

    @property
    def datasets(self) -> list[CatalogDataset]:
        return self._datasets

    @property
    def metrics(self) -> list[CatalogMetric]:
        return self._metrics

    def get_metric(self, metric_id: Union[str, ObjId]) -> CatalogMetric:
        """
        Gets metric by id. The id can be either an instance of ObjId or string containing serialized ObjId
        ('metric/some.metric.id') or contain just the id part ('some.metric.id').

        :param metric_id: fully qualified metric entity id (type/id) or just the identifier of metric entity
        :return: instance of CatalogMetric or None if no such metric in catalog
        :rtype CatalogMetric
        """
        obj_id_str = metric_id

        if isinstance(metric_id, ObjId):
            obj_id_str = str(metric_id)
        elif not metric_id.startswith("metric/"):
            obj_id_str = f"metric/{metric_id}"

        return self._metric_idx[obj_id_str] if obj_id_str in self._metric_idx else None

    def get_dataset(self, dataset_id: Union[str, ObjId]) -> CatalogDataset:
        """
        Gets dataset by id. The id can be either an instance of ObjId or string containing serialized ObjId
        ('dataset/some.dataset.id') or contain just the id part ('some.dataset.id').

        :param dataset_id: fully qualified dataset entity id (type/id) or just the identifier of dataset entity
        :return: instance of CatalogDataset or None if no such dataset in catalog
        :rtype CatalogDataset
        """
        obj_id_str = dataset_id

        if isinstance(dataset_id, ObjId):
            obj_id_str = str(dataset_id)
        elif not dataset_id.startswith("dataset/"):
            obj_id_str = f"dataset/{dataset_id}"

        return (
            self._datasets_idx[obj_id_str] if obj_id_str in self._datasets_idx else None
        )

    def find_label_attribute(self, id_obj) -> Union[CatalogAttribute, None]:
        for dataset in self._datasets:
            res = dataset.find_label_attribute(id_obj)

            if res is not None:
                return res

        return None

    def _valid_objects(self, ctx: ValidObjectsInputType) -> ValidObjects:
        return self._valid_obf_fun(ctx)

    def catalog_with_valid_objects(self, ctx: ValidObjectsInputType):
        """
        Returns a new instance of catalog which contains only those datasets (attributes and facts) that are valid in
        the provided context. The context is composed of one more more entities of the semantic model and
        the filtered catalog will contain only those entities that can be safely added on top of that existing context.

        :param ctx: existing context. you can specify context in one of the following ways:
        - single item or list of items from the execution model
        - single item or list of items from catalog model; catalog fact, label or metric may be added
        - the entire execution definition that is used to compute analytics
        :return:
        """
        valid_objects = self._valid_objects(ctx)

        new_datasets = [
            non_empty
            for non_empty in [d.filter_dataset(valid_objects) for d in self.datasets]
            if non_empty is not None
        ]
        new_metrics = [m for m in self.metrics if m.id in valid_objects[m.type]]

        return Catalog(self._valid_obf_fun, datasets=new_datasets, metrics=new_metrics)

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return f"Catalog(datasets={self.datasets})"


def _create_catalog(valid_obj_fun, datasets, attributes, metrics) -> Catalog:
    # prep: dataset query gets attributes and facts sideloaded, shove them into a map for easier access
    dataset_sideloads = Sideloads(datasets.included)
    attribute_sideloads = Sideloads(attributes.included)

    # metrics are not associated to any dataset, so can construct them right away
    catalog_metrics = [CatalogMetric(metric) for metric in metrics.data]

    # now the rest requires some joins...
    # first construct the dataset's leaves - facts
    catalog_facts = dict(
        [
            (fact["id"], CatalogFact(fact))
            for fact in dataset_sideloads.all_for_type("fact")
        ]
    )

    # then build all attributes & their labels, map them attr.id => attribute
    catalog_attributes = dict()
    for attr in attributes.data:
        attr_id = attr["id"]
        label_ids = attr["relationships"]["labels"]["data"]
        catalog_attributes[attr_id] = CatalogAttribute(
            attr,
            [
                CatalogLabel(attribute_sideloads.find(label_id))
                for label_id in label_ids
            ],
        )

    # finally go through all datasets, find related attributes and facts
    catalog_datasets = dict()
    for dataset in datasets.data:
        dataset_id = dataset["id"]
        rels = dataset["relationships"]
        attribute_ids = rels["attributes"]["data"] if "attributes" in rels else []
        fact_ids = rels["facts"]["data"] if "facts" in rels else []

        catalog_datasets[dataset_id] = CatalogDataset(
            dataset,
            [catalog_attributes[attr_id_obj["id"]] for attr_id_obj in attribute_ids],
            [catalog_facts[fact_id_obj["id"]] for fact_id_obj in fact_ids],
        )

    return Catalog(
        valid_obj_fun=valid_obj_fun,
        datasets=list(catalog_datasets.values()),
        metrics=catalog_metrics,
    )


def _prepare_afm_for_availability(items: list[ValidObjectTypes]):
    attributes = []
    metrics = []
    filters = []

    for item in items:
        if isinstance(item, Attribute):
            attributes.append(item)
        elif isinstance(item, Metric):
            metrics.append(item)
        elif isinstance(item, Filter):
            filters.append(item)
        elif isinstance(item, CatalogLabel):
            attributes.append(item.as_computable())
        elif isinstance(item, (CatalogFact, CatalogMetric)):
            metrics.append(item.as_computable())

    return compute_model_to_api_model(
        attributes=attributes, metrics=metrics, filters=filters
    )


class CatalogService:
    # Note on the disabled checking:
    # generated client has issues parsing the vis objects; .. have to avoid return type checks
    #
    # note: the parsing is done lazily so it does not necessarily bomb on the next line but when trying to
    #  access returned object's properties

    def __init__(self, api_client: GoodDataApiClient):
        self._client = api_client
        self._api = metadata_apis.WorkspaceObjectControllerApi(
            api_client.metadata_client
        )
        self._valid_objects = afm_apis.ValidObjectsControllerApi(api_client.afm_client)

    def get_full_catalog(self, workspace_id: str) -> Catalog:
        """
        Retrieves catalog for a workspace. Catalog contains all data sets and metrics defined in that workspace.

        :param workspace_id: workspace identifier
        :return:
        """
        get_datasets = functools.partial(
            self._api.get_all_entities_datasets,
            workspace_id,
            include=["attributes", "facts"],
            _check_return_type=False,
        )

        get_attributes = functools.partial(
            self._api.get_all_entities_attributes,
            workspace_id,
            include=["labels"],
            _check_return_type=False,
        )

        get_metrics = functools.partial(
            self._api.get_all_entities_metrics, workspace_id, _check_return_type=False
        )

        attributes = load_all_entities(get_attributes)
        datasets = load_all_entities(get_datasets)
        metrics = load_all_entities(get_metrics)

        valid_obj_fun = functools.partial(self.compute_valid_objects, workspace_id)

        return _create_catalog(valid_obj_fun, datasets, attributes, metrics)

    def compute_valid_objects(
        self, workspace_id: str, ctx: ValidObjectsInputType
    ) -> ValidObjects:
        """
        Returns attributes, facts, and metrics which are valid to add to a context that already
        contains some entities from the semantic model. The entities are typically used to compute analytics and
        come from the execution definition. You may, however, specify the entities through different layers of
        convenience.

        :param workspace_id: workspace identifier
        :param ctx: items already in context. you can specify context in one of the following ways:
        - single item or list of items from the execution model
        - single item or list of items from catalog model; catalog fact, label or metric may be added
        - the entire execution definition that is used to compute analytics
        :return: a dict of sets; type of available object is used as key in the dict, the value is a set containing
        id's of available items
        """
        if isinstance(ctx, ExecutionDefinition):
            afm = compute_model_to_api_model(
                attributes=ctx.attributes, metrics=ctx.metrics, filters=ctx.filters
            )
        else:
            _ctx = ctx if isinstance(ctx, list) else [ctx]
            afm = _prepare_afm_for_availability(_ctx)

        query = afm_models.AfmValidObjectsQuery(
            afm=afm, types=["facts", "attributes", "measures"]
        )
        response = self._valid_objects.compute_valid_objects(
            workspace_id=workspace_id, afm_valid_objects_query=query
        )

        by_type: dict[str, set] = dict()

        for available in response.items:
            _type = available["type"]

            if _type not in by_type:
                items_of_type = set()
                by_type[_type] = items_of_type
            else:
                items_of_type = by_type[_type]

            items_of_type.add(available["id"])

        return by_type