.. _ddf:

Main features
*******************************************************************************

Get: G
===============================================================================

The **G** function is the main feature of DDF. It receives a model class and it will return a valid and persisted instance filled with dynamic generated data::


    from django_dynamic_fixture import G, get
    instance = G(MyModel)
    # instance = or get(MyModel)
    print instance.id # this will print the ID, thus the instance was saved
    print instance.some_field # this will print the auto generated data


This will facilitate writing tests and it will hide all dummy data that polute the source code. But all important data of the test scenario must be explicitily defined::


    instance = G(MyModel, my_field=123, another_field='abc')
    print instance.my_field # this will print 123
    print instance.another_field # this will print 'abc'


Important details:

* The id (AutoField) is auto filled, unless you set a value to it.
* if a field has default value, it will be used by default.
* if a field has choices, it select each the first option by default.


New: N
===============================================================================

This function **N** is similar to **G**, except it will not save the generated instance, only all internal dependencies of *ForeignKey* and *OneToOneField* fields. Since the instance does not have an ID, it can not insert instances in *ManyToManyField* fields. This function may be useful mainly in one of the following situations: create a unit test, independent of the database; or
create a not persisted instance that will be manipulated by the programmer before saving it. Usually a programmer may want to manipulate the instance to deal with custom fields, custom validations etc::

    from django_dynamic_fixture import N, new
    instance = N(MyModel)
    # or instance = new(MyModel)
    print instance.id # this will print None
    print instance.some_field # this will print the auto generated data


It is possible to disable saving all instances, but it has to be disabled manually::

    instance = N(MyModel, persist_dependencies=False)
    print instance.id # this will print None
    print instance.some_fk_field.id # this will print None


Fixture: F
===============================================================================

It is possible to explicitly set a value for a field of a dependency (*ForeingKey*, *OneToOneField* and *ManyToManyField*) using the **F** function::

    from django_dynamic_fixture import G, F, fixture
    instance = G(MyModel, my_fk_field=F(my_field=1000))
    # or instance = G(MyModel, my_fk_field=fixture(my_field=1000))
    print instance.my_fk_field.my_field # this will print 1000

This is the equivalent to::

    my_fk_field = G(MyOtherModel, my_field=1000)
    instance = G(MyModel, my_fk_field=my_fk_field)
    print instance.my_fk_field.my_field # this will print 1000

**F** function is recursible::

    instance = G(MyModel, fk_a=F(fk_b=F(field_c=1000)))
    print instance.fk_a.fk_b.field_c # this will print 1000

**F** can be used to customize instances of a ManyToManyField too::

    instance = G(MyModel, many_to_many_field=[F(field_x=1), F(field_x=2)])
    print instance.many_to_many_field.all()[0].field_x # this will print 1
    print instance.many_to_many_field.all()[1].field_x # this will print 2


Many to Many fields
===============================================================================

DDF can add instances in *ManyToManyFields*, but only if the instance has been persisted to the database (Django requirement). DDF deal with *ManyToManyFields* with through too.

It is possible to define how many instances will be created dynamically::

    instance = G(MyModel, many_to_many_field=5)
    print instance.many_to_many_field.all().count() # this will print 5

It is possible to customize each instance of the *ManyToManyField*::

    instance = G(MyModel, many_to_many_field=[F(field_x=10), F(field_y=20)])
    print instance.many_to_many_field.all().count() # this will print 2
    print instance.many_to_many_field.all()[0].field_x # this will print 10
    print instance.many_to_many_field.all()[1].field_y # this will print 20

It is possible to pass already created instances too::

    instance1 = G(MyRelatedModel)
    instance2 = G(MyRelatedModel)

    instance = G(MyModel, many_to_many_field=[instance1, instance2])
    print instance.many_to_many_field.all().count() # this will print 2

    instance = G(MyModel, many_to_many_field=[F(), instance1, F(), instance2])
    print instance.many_to_many_field.all().count() # this will print 4


Django Look Up fields syntax (New in 1.6.1)
===============================================================================

This is an alias to F function, but it follows the Django pattern of filters that use two underlines to access internal fields of foreign keys::

    from django_dynamic_fixture import G
    instance = G(MyModel, myfkfield__myfield=1000)
    print instance.myfkfield__myfield # this will print 1000

Just be careful because DDF do not interpret related names yet.

