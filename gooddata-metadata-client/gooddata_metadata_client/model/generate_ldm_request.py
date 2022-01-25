"""
    OpenAPI definition

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)  # noqa: E501

    The version of the OpenAPI document: v0
    Contact: support@gooddata.com
    Generated by: https://openapi-generator.tech
"""


import re  # noqa: F401
import sys  # noqa: F401

from gooddata_metadata_client.model_utils import (  # noqa: F401
    ApiTypeError,
    ModelComposed,
    ModelNormal,
    ModelSimple,
    cached_property,
    change_keys_js_to_python,
    convert_js_args_to_python_args,
    date,
    datetime,
    file_type,
    none_type,
    validate_get_composed_info,
    OpenApiModel
)
from gooddata_metadata_client.exceptions import ApiAttributeError



class GenerateLdmRequest(ModelNormal):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.

    Attributes:
      allowed_values (dict): The key is the tuple path to the attribute
          and the for var_name this is (var_name,). The value is a dict
          with a capitalized key describing the allowed value and an allowed
          value. These dicts store the allowed enum values.
      attribute_map (dict): The key is attribute name
          and the value is json key in definition.
      discriminator_value_class_map (dict): A dict to go from the discriminator
          variable value to the discriminator class name.
      validations (dict): The key is the tuple path to the attribute
          and the for var_name this is (var_name,). The value is a dict
          that stores validations for max_length, min_length, max_items,
          min_items, exclusive_maximum, inclusive_maximum, exclusive_minimum,
          inclusive_minimum, and regex.
      additional_properties_type (tuple): A tuple of classes accepted
          as additional properties values.
    """

    allowed_values = {
    }

    validations = {
    }

    @cached_property
    def additional_properties_type():
        """
        This must be a method because a model may have properties that are
        of type self, this must run after the class is loaded
        """
        return (bool, date, datetime, dict, float, int, list, str, none_type,)  # noqa: E501

    _nullable = False

    @cached_property
    def openapi_types():
        """
        This must be a method because a model may have properties that are
        of type self, this must run after the class is loaded

        Returns
            openapi_types (dict): The key is attribute name
                and the value is attribute type.
        """
        return {
            'separator': (str,),  # noqa: E501
            'generate_long_ids': (bool,),  # noqa: E501
            'table_prefix': (str,),  # noqa: E501
            'view_prefix': (str,),  # noqa: E501
            'primary_label_prefix': (str,),  # noqa: E501
            'secondary_label_prefix': (str,),  # noqa: E501
            'fact_prefix': (str,),  # noqa: E501
            'date_granularities': (str,),  # noqa: E501
            'grain_prefix': (str,),  # noqa: E501
            'reference_prefix': (str,),  # noqa: E501
            'grain_reference_prefix': (str,),  # noqa: E501
            'denorm_prefix': (str,),  # noqa: E501
            'wdf_prefix': (str,),  # noqa: E501
        }

    @cached_property
    def discriminator():
        return None


    attribute_map = {
        'separator': 'separator',  # noqa: E501
        'generate_long_ids': 'generateLongIds',  # noqa: E501
        'table_prefix': 'tablePrefix',  # noqa: E501
        'view_prefix': 'viewPrefix',  # noqa: E501
        'primary_label_prefix': 'primaryLabelPrefix',  # noqa: E501
        'secondary_label_prefix': 'secondaryLabelPrefix',  # noqa: E501
        'fact_prefix': 'factPrefix',  # noqa: E501
        'date_granularities': 'dateGranularities',  # noqa: E501
        'grain_prefix': 'grainPrefix',  # noqa: E501
        'reference_prefix': 'referencePrefix',  # noqa: E501
        'grain_reference_prefix': 'grainReferencePrefix',  # noqa: E501
        'denorm_prefix': 'denormPrefix',  # noqa: E501
        'wdf_prefix': 'wdfPrefix',  # noqa: E501
    }

    read_only_vars = {
    }

    _composed_schemas = {}

    @classmethod
    @convert_js_args_to_python_args
    def _from_openapi_data(cls, separator, *args, **kwargs):  # noqa: E501
        """GenerateLdmRequest - a model defined in OpenAPI

        Args:
            separator (str): A separator between prefixes and the names. Default is \"__\".

        Keyword Args:
            _check_type (bool): if True, values for parameters in openapi_types
                                will be type checked and a TypeError will be
                                raised if the wrong type is input.
                                Defaults to True
            _path_to_item (tuple/list): This is a list of keys or values to
                                drill down to the model in received_data
                                when deserializing a response
            _spec_property_naming (bool): True if the variable names in the input data
                                are serialized names, as specified in the OpenAPI document.
                                False if the variable names in the input data
                                are pythonic names, e.g. snake case (default)
            _configuration (Configuration): the instance to use when
                                deserializing a file_type parameter.
                                If passed, type conversion is attempted
                                If omitted no type conversion is done.
            _visited_composed_classes (tuple): This stores a tuple of
                                classes that we have traveled through so that
                                if we see that class again we will not use its
                                discriminator again.
                                When traveling through a discriminator, the
                                composed schema that is
                                is traveled through is added to this set.
                                For example if Animal has a discriminator
                                petType and we pass in "Dog", and the class Dog
                                allOf includes Animal, we move through Animal
                                once using the discriminator, and pick Dog.
                                Then in Dog, we will make an instance of the
                                Animal class but this time we won't travel
                                through its discriminator because we passed in
                                _visited_composed_classes = (Animal,)
            generate_long_ids (bool): A flag dictating how the attribute, fact and label ids are generated. By default their ids are derived only from the column name, unless there would be a conflict (e.g. category coming from two different tables). In that case a long id format of <table>.<column> is used. If the flag is set to truethen all ids will be generated in the long form.. [optional]  # noqa: E501
            table_prefix (str): Tables starting with this prefix will be included. The prefix is then followed by the value of `separator` parameter. Given the table prefix is `out_table` and separator is `__`, the table with name like `out_table__customers` will be scanned.. [optional]  # noqa: E501
            view_prefix (str): Views starting with this prefix will be included. The prefix is then followed by the value of `separator` parameter. Given the view prefix is `out_view` and separator is `__`, the table with name like `out_view__us_customers` will be scanned.. [optional]  # noqa: E501
            primary_label_prefix (str): Columns starting with this prefix will be considered as primary labels. The prefix is then followed by the value of `separator` parameter. Given the primary label prefix is `pl` and separator is `__`, the columns with name like `pl__country_id` will be considered as primary labels.. [optional]  # noqa: E501
            secondary_label_prefix (str): Columns starting with this prefix will be considered as secondary labels. The prefix is then followed by the value of `separator` parameter. Given the secondary label prefix is `sl` and separator is `__`, the columns with name like `sl__country_id_country_name` will be considered as secondary labels.. [optional]  # noqa: E501
            fact_prefix (str): Columns starting with this prefix will be considered as facts. The prefix is then followed by the value of `separator` parameter. Given the fact prefix is `f` and separator is `__`, the columns with name like `f__sold` will be considered as facts.. [optional]  # noqa: E501
            date_granularities (str): Option to control date granularities for date datasets. Empty value enables common date granularities (DAY, WEEK, MONTH, QUARTER, YEAR). Default value is `all` which enables all available date granularities, including time granularities (like hours, minutes).. [optional]  # noqa: E501
            grain_prefix (str): Columns starting with this prefix will be considered as grains. The prefix is then followed by the value of `separator` parameter. Given the grain prefix is `g` and separator is `__`, the columns with name like `g__name` will be considered as grains.. [optional]  # noqa: E501
            reference_prefix (str): Columns starting with this prefix will be considered as references. The prefix is then followed by the value of `separator` parameter. Given the reference prefix is `r` and separator is `__`, the columns with name like `r__customer_name` will be considered as references.. [optional]  # noqa: E501
            grain_reference_prefix (str): Columns starting with this prefix will be considered as grain references. The prefix is then followed by the value of `separator` parameter. Given the reference prefix is `gr` and separator is `__`, the columns with name like `gr__customer_name` will be considered as grain references.. [optional]  # noqa: E501
            denorm_prefix (str): Columns starting with this prefix will be considered as denormalization references. The prefix is then followed by the value of `separator` parameter. Given the denormalization reference prefix is `dr` and separator is `__`, the columns with name like `dr__customer_name` will be considered as denormalization references.. [optional]  # noqa: E501
            wdf_prefix (str): Column serving as workspace data filter. No labels are auto generated for such columns.. [optional]  # noqa: E501
        """

        _check_type = kwargs.pop('_check_type', True)
        _spec_property_naming = kwargs.pop('_spec_property_naming', False)
        _path_to_item = kwargs.pop('_path_to_item', ())
        _configuration = kwargs.pop('_configuration', None)
        _visited_composed_classes = kwargs.pop('_visited_composed_classes', ())

        self = super(OpenApiModel, cls).__new__(cls)

        if args:
            raise ApiTypeError(
                "Invalid positional arguments=%s passed to %s. Remove those invalid positional arguments." % (
                    args,
                    self.__class__.__name__,
                ),
                path_to_item=_path_to_item,
                valid_classes=(self.__class__,),
            )

        self._data_store = {}
        self._check_type = _check_type
        self._spec_property_naming = _spec_property_naming
        self._path_to_item = _path_to_item
        self._configuration = _configuration
        self._visited_composed_classes = _visited_composed_classes + (self.__class__,)

        self.separator = separator
        for var_name, var_value in kwargs.items():
            if var_name not in self.attribute_map and \
                        self._configuration is not None and \
                        self._configuration.discard_unknown_keys and \
                        self.additional_properties_type is None:
                # discard variable.
                continue
            setattr(self, var_name, var_value)
        return self

    required_properties = set([
        '_data_store',
        '_check_type',
        '_spec_property_naming',
        '_path_to_item',
        '_configuration',
        '_visited_composed_classes',
    ])

    @convert_js_args_to_python_args
    def __init__(self, separator, *args, **kwargs):  # noqa: E501
        """GenerateLdmRequest - a model defined in OpenAPI

        Args:
            separator (str): A separator between prefixes and the names. Default is \"__\".

        Keyword Args:
            _check_type (bool): if True, values for parameters in openapi_types
                                will be type checked and a TypeError will be
                                raised if the wrong type is input.
                                Defaults to True
            _path_to_item (tuple/list): This is a list of keys or values to
                                drill down to the model in received_data
                                when deserializing a response
            _spec_property_naming (bool): True if the variable names in the input data
                                are serialized names, as specified in the OpenAPI document.
                                False if the variable names in the input data
                                are pythonic names, e.g. snake case (default)
            _configuration (Configuration): the instance to use when
                                deserializing a file_type parameter.
                                If passed, type conversion is attempted
                                If omitted no type conversion is done.
            _visited_composed_classes (tuple): This stores a tuple of
                                classes that we have traveled through so that
                                if we see that class again we will not use its
                                discriminator again.
                                When traveling through a discriminator, the
                                composed schema that is
                                is traveled through is added to this set.
                                For example if Animal has a discriminator
                                petType and we pass in "Dog", and the class Dog
                                allOf includes Animal, we move through Animal
                                once using the discriminator, and pick Dog.
                                Then in Dog, we will make an instance of the
                                Animal class but this time we won't travel
                                through its discriminator because we passed in
                                _visited_composed_classes = (Animal,)
            generate_long_ids (bool): A flag dictating how the attribute, fact and label ids are generated. By default their ids are derived only from the column name, unless there would be a conflict (e.g. category coming from two different tables). In that case a long id format of <table>.<column> is used. If the flag is set to truethen all ids will be generated in the long form.. [optional]  # noqa: E501
            table_prefix (str): Tables starting with this prefix will be included. The prefix is then followed by the value of `separator` parameter. Given the table prefix is `out_table` and separator is `__`, the table with name like `out_table__customers` will be scanned.. [optional]  # noqa: E501
            view_prefix (str): Views starting with this prefix will be included. The prefix is then followed by the value of `separator` parameter. Given the view prefix is `out_view` and separator is `__`, the table with name like `out_view__us_customers` will be scanned.. [optional]  # noqa: E501
            primary_label_prefix (str): Columns starting with this prefix will be considered as primary labels. The prefix is then followed by the value of `separator` parameter. Given the primary label prefix is `pl` and separator is `__`, the columns with name like `pl__country_id` will be considered as primary labels.. [optional]  # noqa: E501
            secondary_label_prefix (str): Columns starting with this prefix will be considered as secondary labels. The prefix is then followed by the value of `separator` parameter. Given the secondary label prefix is `sl` and separator is `__`, the columns with name like `sl__country_id_country_name` will be considered as secondary labels.. [optional]  # noqa: E501
            fact_prefix (str): Columns starting with this prefix will be considered as facts. The prefix is then followed by the value of `separator` parameter. Given the fact prefix is `f` and separator is `__`, the columns with name like `f__sold` will be considered as facts.. [optional]  # noqa: E501
            date_granularities (str): Option to control date granularities for date datasets. Empty value enables common date granularities (DAY, WEEK, MONTH, QUARTER, YEAR). Default value is `all` which enables all available date granularities, including time granularities (like hours, minutes).. [optional]  # noqa: E501
            grain_prefix (str): Columns starting with this prefix will be considered as grains. The prefix is then followed by the value of `separator` parameter. Given the grain prefix is `g` and separator is `__`, the columns with name like `g__name` will be considered as grains.. [optional]  # noqa: E501
            reference_prefix (str): Columns starting with this prefix will be considered as references. The prefix is then followed by the value of `separator` parameter. Given the reference prefix is `r` and separator is `__`, the columns with name like `r__customer_name` will be considered as references.. [optional]  # noqa: E501
            grain_reference_prefix (str): Columns starting with this prefix will be considered as grain references. The prefix is then followed by the value of `separator` parameter. Given the reference prefix is `gr` and separator is `__`, the columns with name like `gr__customer_name` will be considered as grain references.. [optional]  # noqa: E501
            denorm_prefix (str): Columns starting with this prefix will be considered as denormalization references. The prefix is then followed by the value of `separator` parameter. Given the denormalization reference prefix is `dr` and separator is `__`, the columns with name like `dr__customer_name` will be considered as denormalization references.. [optional]  # noqa: E501
            wdf_prefix (str): Column serving as workspace data filter. No labels are auto generated for such columns.. [optional]  # noqa: E501
        """

        _check_type = kwargs.pop('_check_type', True)
        _spec_property_naming = kwargs.pop('_spec_property_naming', False)
        _path_to_item = kwargs.pop('_path_to_item', ())
        _configuration = kwargs.pop('_configuration', None)
        _visited_composed_classes = kwargs.pop('_visited_composed_classes', ())

        if args:
            raise ApiTypeError(
                "Invalid positional arguments=%s passed to %s. Remove those invalid positional arguments." % (
                    args,
                    self.__class__.__name__,
                ),
                path_to_item=_path_to_item,
                valid_classes=(self.__class__,),
            )

        self._data_store = {}
        self._check_type = _check_type
        self._spec_property_naming = _spec_property_naming
        self._path_to_item = _path_to_item
        self._configuration = _configuration
        self._visited_composed_classes = _visited_composed_classes + (self.__class__,)

        self.separator = separator
        for var_name, var_value in kwargs.items():
            if var_name not in self.attribute_map and \
                        self._configuration is not None and \
                        self._configuration.discard_unknown_keys and \
                        self.additional_properties_type is None:
                # discard variable.
                continue
            setattr(self, var_name, var_value)
            if var_name in self.read_only_vars:
                raise ApiAttributeError(f"`{var_name}` is a read-only attribute. Use `from_openapi_data` to instantiate "
                                     f"class with read only attributes.")
